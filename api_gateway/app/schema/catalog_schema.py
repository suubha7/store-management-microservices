from pydantic import BaseModel, Field
from typing import Optional


class CityCreateRequest(BaseModel):
    name: str = Field(min_length=2, max_length=20)


class CityStatusUpdateRequest(BaseModel):
    is_active: bool


class CategoryCreateRequest(BaseModel):
    name: str = Field(min_length=2, max_length=30)
    description: str = Field(min_length=2, max_length=100)


class CategoryUpdateRequest(BaseModel):
    name: Optional[str] = Field(default=None, min_length=2, max_length=30)
    description: Optional[str] = Field(default=None, min_length=2, max_length=100)


class CategoryStatusUpdateRequest(BaseModel):
    is_active: bool


class ProductCreateRequest(BaseModel):
    name: str = Field(min_length=2, max_length=30)
    description: str = Field(min_length=2, max_length=100)
    price: float = Field(ge=0)
    category_id: int = Field(gt=0)


class ProductUpdateRequest(BaseModel):
    name: Optional[str] = Field(default=None, min_length=2, max_length=30)
    description: Optional[str] = Field(default=None, min_length=2, max_length=100)
    price: Optional[float] = Field(default=None, ge=0)
    category_id: Optional[int] = Field(default=None, gt=0)


class ProductStatusUpdateRequest(BaseModel):
    is_active: bool


class CityProductCreateRequest(BaseModel):
    city_id: int = Field(gt=0)
    product_id: int = Field(gt=0)


class CityProductAvailabilityUpdateRequest(BaseModel):
    is_available: bool