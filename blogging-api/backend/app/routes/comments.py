from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database.database import get_db
from app.dependencies.auth import get_current_user
from app.models.post import Post
from app.models.comment import Comment
from app.models.like import Like
from app.models.user import User
from app.schemas.comment import CommentCreate, CommentOut

router = APIRouter(tags=["Comments"])

@router.post("/posts/{post_id}/comments", response_model=CommentOut, status_code=status.HTTP_201_CREATED)
def create_comment(
    post_id: int,
    comment_in: CommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    new_comment = Comment(
        content=comment_in.content,
        post_id=post_id,
        author_id=current_user.id,
    )
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)

    new_comment.author_username = new_comment.author.username
    new_comment.like_count = 0
    new_comment.dislike_count = 0
    new_comment.my_reaction = 0
    return new_comment

@router.get("/posts/{post_id}/comments", response_model=List[CommentOut])
def list_comments_for_post(
    post_id: int,
    db: Session = Depends(get_db),
):
    comments = (
        db.query(Comment)
        .filter(Comment.post_id == post_id)
        .order_by(Comment.id.desc())
        .all()
    )
    if not comments:
        return []

    comment_ids = [c.id for c in comments]

    like_counts = dict(
        db.query(Like.comment_id, func.count(Like.id))
        .filter(Like.comment_id.in_(comment_ids))
        .group_by(Like.comment_id)
        .all()
    )

    for c in comments:
        c.author_username = c.author.username
        c.like_count = int(like_counts.get(c.id, 0))
        c.dislike_count = 0
        c.my_reaction = 0

    return comments

@router.put("/comments/{comment_id}", response_model=CommentOut)
def update_comment(
    comment_id: int,
    comment_in: CommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    if comment.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not allowed")

    comment.content = comment_in.content
    db.commit()
    db.refresh(comment)

    comment.author_username = comment.author.username
    comment.like_count = db.query(Like).filter(Like.comment_id == comment_id).count()
    comment.dislike_count = 0
    comment.my_reaction = 0
    return comment

@router.delete("/comments/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_comment(
    comment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    if comment.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not allowed")

    db.delete(comment)
    db.commit()
    return None
