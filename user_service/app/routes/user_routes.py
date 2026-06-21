from fastapi import APIRouter,Depends, status, HTTPException
from app.auth import hash_password, verify_password
from app.database import get_db
from sqlalchemy.orm import Session 
from app.model import User
from app.schemas import UserRegister, UserLogin


user_router = APIRouter(prefix="/user", tags=["User APIs"])

@user_router.post("/register", status_code=status.HTTP_201_CREATED)
def register_user(user_data: UserRegister, db: Session = Depends(get_db)):

    existing_user = db.query(User).filter(User.email == user_data.email).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        ) 

    
    new_user = User(name = user_data.name,
                    email = user_data.email,
                    hashed_password = hash_password(user_data.password),
                    city_id = user_data.city_id,
                    role = "user"
                    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user


@user_router.post("/login")
def login_user(login_data: UserLogin, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.email == login_data.email).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    is_password_correct = verify_password(login_data.password, user.hashed_password)

    if not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
        )

    return {
        "message": "Login successful",
        "user_id": user.id,
        "role": user.role
    }

