from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime


class CityProductCreate(BaseModel):
    city_id: int = Field(gt=0)
    product_id: int = Field(gt=0)


class CityProductAvailabilityUpdate(BaseModel):
    is_available: bool


class CityProductResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    city_id: int
    product_id: int
    is_available: bool
    created_at: datetime