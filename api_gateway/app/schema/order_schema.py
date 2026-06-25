from pydantic import BaseModel, Field


class CartItemCreateRequest(BaseModel):
    product_id: int = Field(gt=0)
    quantity: int = Field(gt=0)

class CartItemUpdateRequest(BaseModel):
    quantity: int = Field(gt=0)

class CheckoutRequest(BaseModel):
    city_id: int = Field(gt=0)