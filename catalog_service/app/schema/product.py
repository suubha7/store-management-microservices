from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime


class ProductCreate(BaseModel):

    name: str = Field(min_length=2, max_length=30)
    description: str = Field(min_length=2, max_length=100)
    price: float = Field(ge=0)
    category_id: int = Field(gt=0)

class ProductUpdate(BaseModel):

    name: Optional[str] = Field(default=None, min_length=2, max_length=30)
    description: Optional[str] = Field(default=None, min_length=2, max_length=100)
    price: Optional[float] = Field(default=None, ge=0)
    category_id: Optional[int] = Field(default=None, gt=0)

class ProductStatusUpdate(BaseModel):
    is_active: bool

class ProductResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str
    price: float
    category_id: int
    is_active: bool
    created_at: datetime