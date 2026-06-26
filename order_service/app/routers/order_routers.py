from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import httpx
import os
from dotenv import load_dotenv

from app.database import get_db
from app.models import CartItem, Order, OrderItem
from app.dependencies import get_current_user
from app.schema.order_schema import OrderResponse, CheckoutResponse


load_dotenv()

CATALOG_SERVICE_URL = os.getenv("CATALOG_SERVICE_URL")
INVENTORY_SERVICE_URL = os.getenv("INVENTORY_SERVICE_URL")
INTERNAL_SERVICE_KEY = os.getenv("INTERNAL_SERVICE_KEY")

if not INTERNAL_SERVICE_KEY:
    raise RuntimeError("INTERNAL_SERVICE_KEY is missing in .env")

INTERNAL_HEADERS = {"X-Internal-Service-Key": INTERNAL_SERVICE_KEY}


order_router = APIRouter(prefix="/orders",tags=["Order APIs"],dependencies=[Depends(get_current_user)])


@order_router.post("/checkout", response_model=CheckoutResponse, status_code=status.HTTP_201_CREATED)
def checkout(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    user_id = int(current_user["user_id"])

    cart_items = db.query(CartItem).filter(CartItem.user_id == user_id).all()

    if not cart_items:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Cart is empty")

    city_id = cart_items[0].city_id
    for item in cart_items:
        if item.city_id != city_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cart contains items from multiple cities."
            )
    
    product_details = []
    total_amount = 0.0

    for cart_item in cart_items:
        try:
            catalog_response = httpx.get(
                f"{CATALOG_SERVICE_URL}/catalog/products/{cart_item.product_id}",
                timeout=5.0
            )
        except httpx.ConnectError:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Catalog Service is not running or cannot be reached"
            )

        if catalog_response.status_code == status.HTTP_404_NOT_FOUND:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product {cart_item.product_id} not found"
            )

        if catalog_response.status_code != status.HTTP_200_OK:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Catalog Service is unavailable"
            )

        product_data = catalog_response.json()

        if not product_data["is_active"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Product {cart_item.product_id} is inactive"
            )

        stock_request_data = {
            "city_id": city_id,
            "product_id": cart_item.product_id,
            "quantity": cart_item.quantity
        }

        try:
            stock_response = httpx.post(
                f"{INVENTORY_SERVICE_URL}/inventory/check-stock",
                json=stock_request_data,
                headers=INTERNAL_HEADERS,
                timeout=5.0
            )
        except httpx.ConnectError:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Inventory Service is not running or cannot be reached"
            )

        if stock_response.status_code == status.HTTP_404_NOT_FOUND:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Inventory not found for product {cart_item.product_id} in this city"
            )

        if stock_response.status_code == status.HTTP_403_FORBIDDEN:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Order Service is not authorized to access Inventory Service")

        if stock_response.status_code != status.HTTP_200_OK:
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Inventory Service is unavailable")

        stock_data = stock_response.json()

        if not stock_data["available"]:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Insufficient stock for product {cart_item.product_id}")
                
            

        price = product_data["price"]
        subtotal = price * cart_item.quantity

        product_details.append({
            "product_id": cart_item.product_id,
            "product_name": product_data["name"],
            "price": price,
            "quantity": cart_item.quantity,
            "subtotal": subtotal
        })

        total_amount += subtotal

    for product in product_details:
        try:
            reduce_stock_response = httpx.post(
                f"{INVENTORY_SERVICE_URL}/inventory/reduce-stock",
                json={
                    "city_id": city_id,
                    "product_id": product["product_id"],
                    "quantity": product["quantity"]
                },
                headers=INTERNAL_HEADERS,
                timeout=5.0
            )
        except httpx.ConnectError:
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Inventory Service is not running or cannot be reached")

        if reduce_stock_response.status_code == status.HTTP_400_BAD_REQUEST:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Insufficient stock for product {product['product_id']}")

        if reduce_stock_response.status_code == status.HTTP_403_FORBIDDEN:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Order Service is not authorized to access Inventory Service")

        if reduce_stock_response.status_code != status.HTTP_200_OK:
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Could not reduce inventory stock")

    new_order = Order(user_id=user_id, city_id= city_id, total_amount=total_amount, status="pending")

    db.add(new_order)
    db.flush()

    for product in product_details:
        new_order_item = OrderItem(
            order_id=new_order.id,
            product_id=product["product_id"],
            product_name=product["product_name"],
            price=product["price"],
            quantity=product["quantity"],
            subtotal=product["subtotal"]
        )

        db.add(new_order_item)

    db.query(CartItem).filter(CartItem.user_id == user_id).delete()

    db.commit()
    db.refresh(new_order)

    return new_order


@order_router.get("", response_model=list[OrderResponse])
def get_my_orders(db: Session = Depends(get_db),current_user: dict = Depends(get_current_user)):
    user_id = int(current_user["user_id"])

    orders = db.query(Order).filter(Order.user_id == user_id).all()

    return orders


@order_router.get("/{order_id}", response_model=CheckoutResponse)
def get_my_order_by_id(order_id: int,db: Session = Depends(get_db),current_user: dict = Depends(get_current_user)):
    user_id = int(current_user["user_id"])

    order = db.query(Order).filter(Order.id == order_id,Order.user_id == user_id).first()

    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Order not found")

    return order