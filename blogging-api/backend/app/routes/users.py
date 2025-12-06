from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate, UserOut
from app.database.database import get_db

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register_user(user_in: UserCreate, db: Session = Depends(get_db)):

    #Register new user
    existing_email = db.query(User).filter(User.email == user_in.email).first()
    if existing_email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    
    existing_username = db.query(User).filter(User.name == user_in.name).first()
    if existing_username:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail="Username already taken")
    
    new_user = User(
        username = user_in.username,
        email = user_in.email,
        password = user_in.password,
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.get("/", response_model=List[UserOut])
def list_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users