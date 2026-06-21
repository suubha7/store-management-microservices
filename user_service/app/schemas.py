from pydantic import BaseModel, Field, EmailStr
from typing import Literal, Optional
from datetime import datetime



class UserRegister(BaseModel):
    name: str = Field(min_length=2, max_length=40)
    email: EmailStr
    password: str = Field(min_length=6, max_length=40)
    city_id: int = Field(gt= 0)


class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6, max_length=40)

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    city_id: int
    role: Literal["user", "admin"]
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=2, max_length=100)
    city_id: Optional[int] = Field(default=None, gt=0)
    password: Optional[str] = Field(default=None, min_length=6, max_length=50)

class UserStatusUpdate(BaseModel):
    is_active: bool