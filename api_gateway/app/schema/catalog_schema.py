from pydantic import BaseModel, Field
from typing import Optional


# Schema for creating a city request
class CityCreateRequest(BaseModel):
    name: str = Field(min_length=2, max_length=20)


# Schema for updating city status request
class CityStatusUpdateRequest(BaseModel):
    is_active: bool


# Schema for creating a category request
class CategoryCreateRequest(BaseModel):
    name: str = Field(min_length=2, max_length=30)
    description: str = Field(min_length=2, max_length=100)


# Schema for updating a category request
class CategoryUpdateRequest(BaseModel):
    name: Optional[str] = Field(default=None, min_length=2, max_length=30)
    description: Optional[str] = Field(default=None, min_length=2, max_length=100)


# Schema for updating category status request
class CategoryStatusUpdateRequest(BaseModel):
    is_active: bool


# Schema for creating a product request
class ProductCreateRequest(BaseModel):
    name: str = Field(min_length=2, max_length=30)
    description: str = Field(min_length=2, max_length=100)
    price: float = Field(ge=0)
    category_id: int = Field(gt=0)


# Schema for updating a product request
class ProductUpdateRequest(BaseModel):
    name: Optional[str] = Field(default=None, min_length=2, max_length=30)
    description: Optional[str] = Field(default=None, min_length=2, max_length=100)
    price: Optional[float] = Field(default=None, ge=0)
    category_id: Optional[int] = Field(default=None, gt=0)


# Schema for updating product status request
class ProductStatusUpdateRequest(BaseModel):
    is_active: bool


# Schema for creating a city product mapping request
class CityProductCreateRequest(BaseModel):
    city_id: int = Field(gt=0)
    product_id: int = Field(gt=0)


# Schema for updating city product availability request
class CityProductAvailabilityUpdateRequest(BaseModel):
    is_available: bool