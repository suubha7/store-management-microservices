from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime


# Schema for creating a cart item
class CartItemCreate(BaseModel):
    product_id: int = Field(gt=0)
    quantity: int = Field(gt=0)
    city_id: int = Field(gt=0)


# Schema for updating a cart item
class CartItemUpdate(BaseModel):
    quantity: int = Field(gt=0)


# Schema for cart item response
class CartItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    product_id: int
    quantity: int
    created_at: datetime
    updated_at: datetime