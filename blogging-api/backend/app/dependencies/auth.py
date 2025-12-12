from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt

from app.database.database import get_db
from app.models.user import User
from app.utils.auth import SECRET_KEY, ALGORITHM

#This is used to extract token from request header
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) ->User:
    # Extract JWT token , decode it, then return it to current user from database
    try:
        # Decode the token to get User ID
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("sub") # get sub claim which is user_id

        if user_id is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Token", headers={"WWW-Authenticate": "Bearer"})

        user = db.query(User).filter(User.id == user_id).first()

        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found", headers={"WWW-Authenticate": "Bearer"})
        
        return user
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token", headers={"WWW-Authenticate": "Bearer"})
    
        

