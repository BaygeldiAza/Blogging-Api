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
    comments =  db.query(Comment).filter(Comment.post_id == post_id).all()

    # Add author_username to each comment
    for comment in comments:
        comment.author_username = comment.author.username

    return comments

@router.put("/{comment_id}", response_model=CommentOut)
def update_comment(comment_id: int, comment_in: CommentCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    #chech whether comment exists
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")
    # ensure the current user is the author of the comment
    if comment.author_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to edit this comment")
    
    comment.content = comment_in.content
    db.commit()
    db.refresh(comment)

    return comment 

@router.delete("/{comment_id}", status_code=status.HTTP_404_NOT_FOUND)
def delete_comment(comment_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    #check whether the comment exists
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")
    #ensure current user is the author of this comment
    if comment.author_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this comment")
    
    db.delete(comment)
    db.commit()

    return None