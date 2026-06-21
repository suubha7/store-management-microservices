from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.model import User
from app.database import get_db
from app.schemas import UserResponse, UserStatusUpdate


admin_router = APIRouter(prefix="/admin", tags=["Admin APIs"])

@admin_router.get("/users", response_model=list[UserResponse])
def all_users(db: Session = Depends(get_db)):

    users = db.query(User).all()

    return users

@admin_router.get("/user/{user_id}", response_model= UserResponse)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    return user

@admin_router.put("/user/update_status/{user_id}", response_model=UserResponse)
def update_user_status_by_id(user_id: int, user_status: UserStatusUpdate, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    user.is_active = user_status.is_active
    db.commit() 
    db.refresh(user)

    return user

@admin_router.delete("/user/delete/{user_id}", status_code=status.HTTP_200_OK)
def delete_user_by_id(user_id: int, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    db.delete(user)
    db.commit()

    return {"message": "User deleted successfully"}



