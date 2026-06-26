from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime

# Schema for creating inventory
class CreateInventory(BaseModel):

    city_id: int = Field(gt=0)
    product_id: int = Field(gt=0)
    stock_quantity: int = Field(ge=0)

# Schema for updating inventory stock
class InventoryStockUpdate(BaseModel):

    stock_quantity: int = Field(ge=0)

# Schema for inventory response
class InventoryResponse(BaseModel):
    model_config = ConfigDict(from_attributes= True)

    city_id: int
    product_id: int 
    stock_quantity: int

    created_at: datetime
    updated_at: datetime

# Schema for checking or updating stock
class StockRequest(BaseModel):
    city_id: int = Field(gt=0)
    product_id: int = Field(gt=0)
    quantity: int = Field(gt=0)

# Schema for stock response
class StockResponse(BaseModel):
    available: bool
    stock_quantity: int


