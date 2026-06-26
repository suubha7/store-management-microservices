from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Inventory
from app.schema.inventory_schema import StockRequest, StockResponse
from app.internal_dependencies import verify_internal_service_key


inventory_internal_router = APIRouter(
    prefix="/inventory",
    tags=["Inventory Internal APIs"],
    dependencies=[Depends(verify_internal_service_key)]
)


# Check product stock level
@inventory_internal_router.post("/check-stock", response_model=StockResponse,status_code=status.HTTP_200_OK)
def check_stock(stock_data: StockRequest, db: Session = Depends(get_db)):
    inventory = db.query(Inventory).filter(
        Inventory.city_id == stock_data.city_id,
        Inventory.product_id == stock_data.product_id
    ).first()

    if not inventory:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Inventory record not found")

    available = inventory.stock_quantity >= stock_data.quantity

    return {
        "available": available,
        "stock_quantity": inventory.stock_quantity
    }


# Reduce product stock quantity
@inventory_internal_router.post("/reduce-stock", response_model=StockResponse, status_code=status.HTTP_200_OK)
def reduce_stock(stock_data: StockRequest, db: Session = Depends(get_db)):
    inventory = db.query(Inventory).filter(
        Inventory.city_id == stock_data.city_id,
        Inventory.product_id == stock_data.product_id
    ).first()

    if not inventory:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Inventory record not found")

    if inventory.stock_quantity < stock_data.quantity:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Insufficient stock")

    inventory.stock_quantity -= stock_data.quantity

    db.commit()
    db.refresh(inventory)

    return {
        "available": True,
        "stock_quantity": inventory.stock_quantity
    }