from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime


class CategoryCreate(BaseModel):

    name: str = Field(min_length=2, max_length=30)
    description: str = Field(min_length=2, max_length=100)

class CategoryUpdate(BaseModel):

    name: Optional[str] = Field(default=None, min_length=2, max_length=30)
    description: Optional[str] = Field(default=None, min_length=2, max_length=100)

class CategoryStatusUpdate(BaseModel):
    is_active: bool

class CategoryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int 
    name: str
    description: str
    is_active: bool
    created_at: datetime