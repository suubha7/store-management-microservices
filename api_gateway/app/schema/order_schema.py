from pydantic import BaseModel, Field


# Schema for creating a cart item request
class CartItemCreateRequest(BaseModel):
    product_id: int = Field(gt=0)
    quantity: int = Field(gt=0)
    city_id: int = Field(gt=0)

# Schema for updating a cart item request
class CartItemUpdateRequest(BaseModel):
    quantity: int = Field(gt=0)
