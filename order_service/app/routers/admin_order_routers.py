from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Order
from app.dependencies import require_admin
from app.schema.order_schema import OrderResponse, CheckoutResponse


admin_order_router = APIRouter(prefix="/admin",tags=["Admin Order APIs"],dependencies=[Depends(require_admin)])


@admin_order_router.get("/orders", response_model=list[OrderResponse])
def get_all_orders(db: Session = Depends(get_db)):
    orders = db.query(Order).all()

    return orders


@admin_order_router.get("/orders/{order_id}", response_model=CheckoutResponse)
def get_order_by_id(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()

    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Order not found")

    return order