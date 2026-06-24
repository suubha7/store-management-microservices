from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime

class CreateInventory(BaseModel):

    city_id: int = Field(gt=0)
    product_id: int = Field(gt=0)
    stock_quantity: int = Field(ge=0)

class InventoryStockUpdate(BaseModel):

    stock_quantity: int = Field(ge=0)

class InventoryResponse(BaseModel):
    model_config = ConfigDict(from_attributes= True)

    city_id: int
    product_id: int 
    stock_quantity: int

    created_at: datetime
    updated_at: datetime

class StockRequest(BaseModel):
    city_id: int = Field(gt=0)
    product_id: int = Field(gt=0)
    quantity: int = Field(gt=0)

class StockResponse(BaseModel):
    available: bool
    stock_quantity: int


