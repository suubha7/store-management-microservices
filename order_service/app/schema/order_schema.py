from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import List



class OrderItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    product_id: int
    product_name: str
    price: float
    quantity: int
    subtotal: float


class OrderResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    city_id: int
    total_amount: float
    status: str
    created_at: datetime
    updated_at: datetime


class CheckoutResponse(OrderResponse):
    order_items: List[OrderItemResponse]