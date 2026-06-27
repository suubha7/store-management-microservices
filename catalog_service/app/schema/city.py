from pydantic import BaseModel, Field, ConfigDict
from typing import Optional


# Schema for creating a city
class CityCreate(BaseModel):

    name: str = Field(min_length=2, max_length=20)

# Schema for updating city status
class CityStatusUpdate(BaseModel):
    is_active: bool

# Schema for city response
class CityResponse(CityStatusUpdate, CityCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int 
