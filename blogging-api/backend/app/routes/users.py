from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from app.models.user import User
from app.schemas.user import UserCreate, UserOut
from app.database.database import get_db
from app.utils.password import hash_password, verify_password
from app.utils.auth import create_access_token
from app.dependencies.auth import get_current_user

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register_user(user_in: UserCreate, db: Session = Depends(get_db)):

    #Register new user
    existing_email = db.query(User).filter(User.email == user_in.email).first()
    if existing_email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    
    existing_username = db.query(User).filter(User.username == user_in.name).first()
    if existing_username:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail="Username already taken")
    
    new_user = User(
        username = user_in.username,
        email = user_in.email,
        password = hash_password(user_in.password),
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    #Login the user by verifining their credentials and returning a JWT token
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect email or password")
    
    #Verify password
    if not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect email or password")
    
    # Gerenate new JWT token 
    access_token = create_access_token(data={"sub": user.email})

    return{"access_token": access_token, "token_type": "bearer"}

router.get("/me", response_model=UserOut)
def read_me(current_user: User = Depends(get_current_user)):
    #Protected endpoint returns the currently logged-in user's information
    return current_user


@router.get("/", response_model=List[UserOut])
def list_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users

