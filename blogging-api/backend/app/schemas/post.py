from pydantic import BaseModel, ConfigDict

#Shared fields for creating and returning to client
class PostBase(BaseModel):
    title: str
    content: str
#Create new post(request body)
class PostCreate(PostBase):
    pass 
#Return a post to the client(response body)
class PostOut(PostBase):
    id: int 
    author_id: int

    class Config:
        config_model = ConfigDict(from_attributes=True)