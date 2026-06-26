from pydantic import BaseModel, Field, EmailStr
from typing import Optional


# Schema for user registration request
class UserRegisterRequest(BaseModel):
    name: str = Field(min_length=2, max_length=40)
    email: EmailStr
    password: str = Field(min_length=6, max_length=40)
    city_id: int = Field(gt=0)


# Schema for updating user profile request
class UserUpdateRequest(BaseModel):
    name: Optional[str] = Field(default=None, min_length=2, max_length=100)
    city_id: Optional[int] = Field(default=None, gt=0)


# Schema for updating user status request
class UserStatusUpdateRequest(BaseModel):
    is_active: bool


# Schema for password change request
class ChangePasswordRequest(BaseModel):
    current_password: str = Field(min_length=6, max_length=50)
    new_password: str = Field(min_length=6, max_length=50)

# Schema for updating user status request
class UserStatusUpdateRequest(BaseModel):
    is_active: bool