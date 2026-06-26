from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import CartItem
from app.dependencies import get_current_user
from app.schema.cart_schema import CartItemCreate, CartItemUpdate, CartItemResponse



cart_router = APIRouter(prefix="/cart", tags=["Cart APIs"],dependencies=[Depends(get_current_user)])


# Add a new item to cart
@cart_router.post("/items", response_model=CartItemResponse, status_code=status.HTTP_201_CREATED)
def create_cart_item(cart_data: CartItemCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    user_id = int(current_user["user_id"])

    # Check whether the cart already contains items
    existing_cart = db.query(CartItem).filter(CartItem.user_id == user_id).first()

    if existing_cart:
        if existing_cart.city_id != cart_data.city_id:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Your cart contains items from another city. Please clear the cart first.")

    existing_cart_item = db.query(CartItem).filter(CartItem.user_id == user_id, CartItem.product_id == cart_data.product_id).first()

    if existing_cart_item:
        existing_cart_item.quantity += cart_data.quantity

        db.commit()
        db.refresh(existing_cart_item)

        return existing_cart_item

    new_cart_item = CartItem(
        user_id=user_id,
        product_id=cart_data.product_id,
        city_id=cart_data.city_id,
        quantity=cart_data.quantity
    )

    db.add(new_cart_item)
    db.commit()
    db.refresh(new_cart_item)

    return new_cart_item


# Retrieve items in current cart
@cart_router.get("", response_model=list[CartItemResponse])
def get_cart_items(db: Session = Depends(get_db),current_user: dict = Depends(get_current_user)):
    user_id = int(current_user["user_id"])

    cart_items = db.query(CartItem).filter(CartItem.user_id == user_id).all()

    return cart_items


# Update quantity of cart item
@cart_router.put("/items/{cart_item_id}",response_model=CartItemResponse)
def update_cart_item(
    cart_item_id: int,
    cart_data: CartItemUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    user_id = int(current_user["user_id"])

    cart_item = db.query(CartItem).filter(CartItem.id == cart_item_id,CartItem.user_id == user_id).first()

    if not cart_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart item not found")

    cart_item.quantity = cart_data.quantity

    db.commit()
    db.refresh(cart_item)

    return cart_item


# Remove item from cart
@cart_router.delete("/items/{cart_item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_cart_item(
    cart_item_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    user_id = int(current_user["user_id"])

    cart_item = db.query(CartItem).filter(CartItem.id == cart_item_id, CartItem.user_id == user_id).first()

    if not cart_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart item not found")

    db.delete(cart_item)
    db.commit()


# Remove all items from cart
@cart_router.delete("/clear",status_code=status.HTTP_204_NO_CONTENT)
def clear_cart(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    user_id = int(current_user["user_id"])

    db.query(CartItem).filter(CartItem.user_id == user_id).delete()

    db.commit()