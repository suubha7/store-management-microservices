from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import List



# Schema for order item response
class OrderItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    product_id: int
    product_name: str
    price: float
    quantity: int
    subtotal: float


# Schema for order response
class OrderResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    city_id: int
    total_amount: float
    status: str
    created_at: datetime
    updated_at: datetime


# Schema for checkout response
class CheckoutResponse(OrderResponse):
    order_items: List[OrderItemResponse]