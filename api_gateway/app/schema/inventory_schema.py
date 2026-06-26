from pydantic import BaseModel, Field


# Schema for creating inventory request
class CreateInventoryRequest(BaseModel):
    city_id: int = Field(gt=0)
    product_id: int = Field(gt=0)
    stock_quantity: int = Field(ge=0)


# Schema for updating inventory stock request
class InventoryStockUpdateRequest(BaseModel):
    stock_quantity: int = Field(ge=0)