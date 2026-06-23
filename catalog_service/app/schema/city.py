from pydantic import BaseModel, Field, ConfigDict
from typing import Optional


class CityCreate(BaseModel):

    name: str = Field(min_length=2, max_length=20)

class CityStatusUpdate(BaseModel):
    is_active: bool

class CityResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int 
    name: str
    is_active: bool