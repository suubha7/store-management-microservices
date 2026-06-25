from pydantic import BaseModel, Field


class CreateInventoryRequest(BaseModel):
    city_id: int = Field(gt=0)
    product_id: int = Field(gt=0)
    stock_quantity: int = Field(ge=0)


class InventoryStockUpdateRequest(BaseModel):
    stock_quantity: int = Field(ge=0)