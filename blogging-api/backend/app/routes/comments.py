from typing import List

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func, case 

from app.models.user import User
from app.models.post import Post
from app.models.comment import Comment
from app.models.like import Like
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
        post_id = comment_in.post_id,
        author_id = current_user.id,
    )

    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)

    new_comment.author_username = new_comment.author.username
    new_comment.like_count = 0
    new_comment.dislike_count = 0

    return new_comment

@router.get("/post/{post_id}", response_model=List[CommentOut])
def list_comments_for_post(post_id: int, db: Session=Depends(get_db), limit: int = 10, skip: int = 0):
    #Retrieve comments for post 
    comments =  db.query(Comment).filter(Comment.post_id == post_id).order_by(Comment.id.desc()).offset(skip).limit(limit).all()

    if not comments:
        return []
    
    comment_ids = [c.id for c in comments]

    counts = (
        db.query(Like.comment_id.label("comment_id"),
                 func.sum(case((Like.value == 1, 1), else_=0)).label("like_count"),
                 func.sum(case((Like.value == -1, 1), else_=0)).label("dislike_count"),
                 )
                .filter(Like.comment_id.in_(comment_ids))
                .group_by(Like.comment_id)
                .all()
    )

    counts_map = {
        row.comment_id: (int(row.like_count or 0), int(row.dislike_count or 0))
        for row in counts
    }

    # Add author_username to each comment
    for comment in comments:
        comment.author_username = comment.author.username
        like_count, dislike_count = counts_map.get(comment.id, (0, 0))
        comment.like_count = like_count
        comment.dislike_count = dislike_count

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

    comment.author_username = comment.author.username   
    comment.like_count = 0
    comment.dislike_count = 0

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