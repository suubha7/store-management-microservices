from pydantic import BaseModel, Field, EmailStr
from typing import Optional


class UserRegisterRequest(BaseModel):
    name: str = Field(min_length=2, max_length=40)
    email: EmailStr
    password: str = Field(min_length=6, max_length=40)
    city_id: int = Field(gt=0)


class UserUpdateRequest(BaseModel):
    name: Optional[str] = Field(default=None, min_length=2, max_length=100)
    city_id: Optional[int] = Field(default=None, gt=0)


class UserStatusUpdateRequest(BaseModel):
    is_active: bool


class ChangePasswordRequest(BaseModel):
    current_password: str = Field(min_length=6, max_length=50)
    new_password: str = Field(min_length=6, max_length=50)

class UserStatusUpdateRequest(BaseModel):
    is_active: bool