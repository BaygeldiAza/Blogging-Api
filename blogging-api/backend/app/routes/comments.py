from typing import List
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status
from app.models.user import User
from app.models.post import Post
from app.models.comment import Comment
from app.database.database import get_db
from app.dependencies.auth import get_current_user
from app.schemas.comment import CommentCreate, CommentOut

router = APIRouter(prefix="/comments", tags=["Comments"])

@router.post("/", response_model=CommentOut, status_code=status.HTTP_201_CREATED)
def create_comment(comment_in: CommentCreate, db: Session=Depends(get_db), current_user: User=Depends(get_current_user)):
    # Make sure comment exists
    post = db.query(Post).filter(Post.id == comment_in.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    
    new_comment = Comment(
        content = comment_in.content,
        post_id = comment_in.post,
        author_id = current_user.id,
    )

    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)

    return new_comment

@router.get("/post/{post_id}", response_model=List[CommentOut])
def list_comments_for_post(post_id: int, db: Session=Depends(get_db)):
    #Retrieve comments for post 
    return db.query(Comment).filter(Comment.post_id == post_id).all()
