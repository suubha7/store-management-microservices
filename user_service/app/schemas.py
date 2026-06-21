from pydantic import BaseModel, Field, EmailStr



class UserRegister(BaseModel):
    name: str = Field(min_length=2, max_length=40)
    email: EmailStr
    password: str = Field(min_length=6, max_length=40)
    city_id: int = Field(gt= 0)


class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6, max_length=40)
    
