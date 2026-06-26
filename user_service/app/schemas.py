from pydantic import BaseModel, Field, EmailStr
from typing import Literal, Optional
from datetime import datetime



# Schema for user registration
class UserRegister(BaseModel):
    name: str = Field(min_length=2, max_length=40)
    email: EmailStr
    password: str = Field(min_length=6, max_length=40)
    city_id: int = Field(gt= 0)


# Schema for user login
class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6, max_length=40)

# Schema for user response
class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    city_id: int
    role: Literal["user", "admin"]
    is_active: bool
    created_at: datetime

    # Pydantic configuration settings
    class Config:
        from_attributes = True

# Schema for updating user profile
class UserUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=2, max_length=100)
    city_id: Optional[int] = Field(default=None, gt=0)

# Schema for updating user status
class UserStatusUpdate(BaseModel):
    is_active: bool

# Schema for authentication token response
class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    role: Literal["user", "admin"]

# Schema for password change request
class ChangePasswordRequest(BaseModel):
    current_password: str = Field(min_length=6, max_length=50)
    new_password: str = Field(min_length=6, max_length=50)