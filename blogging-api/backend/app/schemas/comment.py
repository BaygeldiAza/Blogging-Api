from pydantic import BaseModel, ConfigDict

class CommentBase(BaseModel):
    content: str

class CommentCreate(CommentBase):
    post_id: int

class CommentOut(CommentBase):
    id: int
    author_id: int
    post_id: int

    class Config:
        config_model = ConfigDict(from_attributes=True)