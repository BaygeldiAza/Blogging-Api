from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.database.database import get_db
from app.dependencies.auth import get_current_user
from app.models.like import Like
from app.models.post import Post
from app.models.comment import Comment
from app.models.user import User
from app.schemas.like import LikeCreate

router = APIRouter(prefix="/likes", tags=["Likes"])

@router.post("/", status_code=status.HTTP_201_CREATED)
def like_target(
    payload: LikeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if (payload.post_id is None) == (payload.comment_id is None):
        raise HTTPException(status_code=400, detail="Send exactly one: post_id OR comment_id")

    if payload.post_id is not None:
        post = db.query(Post).filter(Post.id == payload.post_id).first()
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")

        like = Like(user_id=current_user.id, post_id=payload.post_id)

    else:
        comment = db.query(Comment).filter(Comment.id == payload.comment_id).first()
        if not comment:
            raise HTTPException(status_code=404, detail="Comment not found")

        like = Like(user_id=current_user.id, comment_id=payload.comment_id)

    db.add(like)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        # idempotent: already liked
        return {"detail": "Already liked"}

    return {"detail": "Liked"}

@router.delete("/post/{post_id}", status_code=status.HTTP_200_OK)
def unlike_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    existing = db.query(Like).filter(Like.post_id == post_id, Like.user_id == current_user.id).first()
    if not existing:
        raise HTTPException(status_code=404, detail="Like not found")

    db.delete(existing)
    db.commit()
    return {"detail": "Unliked"}

@router.delete("/comment/{comment_id}", status_code=status.HTTP_200_OK)
def unlike_comment(
    comment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    existing = db.query(Like).filter(Like.comment_id == comment_id, Like.user_id == current_user.id).first()
    if not existing:
        raise HTTPException(status_code=404, detail="Like not found")

    db.delete(existing)
    db.commit()
    return {"detail": "Unliked"}

# Optional compatibility with your frontend if it calls DELETE /likes/{post_id}
@router.delete("/{post_id}", status_code=status.HTTP_200_OK)
def unlike_post_compat(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    existing = db.query(Like).filter(Like.post_id == post_id, Like.user_id == current_user.id).first()
    if not existing:
        raise HTTPException(status_code=404, detail="Like not found")
    db.delete(existing)
    db.commit()
    return {"detail": "Unliked"}
