from pydantic import BaseModel, ConfigDict


class CommentCreate(BaseModel):
    content: str


class CommentOut(BaseModel):
    id: int
    content: str
    author_id: int
    post_id: int
    author_username: str

    like_count: int = 0
    dislike_count: int = 0  # kept for compatibility
    my_reaction: int = 0    # 1 if liked else 0

    model_config = ConfigDict(from_attributes=True)
