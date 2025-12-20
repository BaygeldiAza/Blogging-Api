from pydantic import BaseModel, ConfigDict


class PostBase(BaseModel):
    title: str
    content: str


class PostCreate(PostBase):
    pass


class PostOut(PostBase):
    id: int
    author_id: int
    author_username: str

    comment_count: int = 0
    like_count: int = 0
    dislike_count: int = 0  # kept for compatibility if frontend expects it

    liked_by_me: bool = False

    # optional aliases for some frontends
    likes_count: int = 0
    comments_count: int = 0

    model_config = ConfigDict(from_attributes=True)
