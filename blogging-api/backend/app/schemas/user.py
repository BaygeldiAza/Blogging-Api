from pydantic import BaseModel, ConfigDict, EmailStr

class UserBase(BaseModel):
    username: str
    email: EmailStr  #checks whether email or not 

class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    id: int

    class Config:
        model_config = ConfigDict(from_attributes=True)