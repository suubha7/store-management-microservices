from sqlalchemy import Column, String, Integer, Boolean, DateTime
from datetime import datetime
from app.database import Base

# User database model
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key= True, index=True)
    name = Column(String(30), nullable=False)
    email = Column(String(50), unique=True, index=True, nullable=False)
    hashed_password = Column(String(300), nullable=False)
    city_id = Column(Integer, nullable=False)
    role = Column(String(10),nullable=False, default="user")
    is_active = Column(Boolean, default=True)
    created_at = Column(
        DateTime,
        default=datetime.now
    )