from fastapi import APIRouter,Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from app.auth import hash_password, verify_password
from app.database import get_db
from sqlalchemy.orm import Session 
from app.model import User
from app.schemas import UserRegister, UserLogin, UserResponse, UserUpdate, TokenResponse, ChangePasswordRequest
from app.auth import create_access_token
from app.dependencies import get_current_user


user_router = APIRouter(prefix="/user", tags=["User APIs"])

@user_router.post("/register",response_model=UserResponse, status_code=status.HTTP_201_CREATED)
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


@user_router.post("/login", response_model= TokenResponse)
def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    user = db.query(User).filter(User.email == form_data.username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    is_password_correct = verify_password(form_data.password, user.hashed_password)

    if not is_password_correct:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
        )
    access_token = create_access_token( user_id=user.id, role=user.role )

    return { "access_token": access_token, "token_type": "bearer", "role": user.role }

@user_router.get("/me", response_model=UserResponse, status_code=status.HTTP_200_OK)
def get_my_profile(db: Session= Depends(get_db), current_user: dict = Depends(get_current_user)):

    user = db.query(User).filter(User.id == current_user["user_id"]).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    return user


@user_router.put("/me", response_model= UserResponse, status_code=status.HTTP_200_OK)
def update_my_profile(user_data: UserUpdate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):

    user = db.query(User).filter(User.id == current_user["user_id"]).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not Found")
    
    if user_data.name is not None:
        user.name = user_data.name

    if user_data.city_id is not None:
        user.city_id = user_data.city_id

    db.commit() 
    db.refresh(user)

    return user

@user_router.put("/me/password", status_code=status.HTTP_200_OK)
def change_my_password(password_data: ChangePasswordRequest, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):

    user = db.query(User).filter(User.id == current_user["user_id"]).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not Found")
    
    is_current_password_correct = verify_password(password_data.current_password, user.hashed_password)

    if not is_current_password_correct:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Current password is incorrect"
        )
    
    user.hashed_password = hash_password(password_data.new_password)

    db.commit() 
    db.refresh(user)

    return {
        "message": "Password updated successfully"
    }