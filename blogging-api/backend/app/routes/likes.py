from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.dependencies.auth import get_current_user
from app.models.comment import Comment  
from app.models.user import User
from app.models.like import Like

router = APIRouter(prefix="/likes", tags=["Likes"])

@router.post("/comment/{comment_id}")
def like_or_dislike_comment(comment_id: int, value: int, db: Session=Depends(get_db), current_user: User=Depends(get_current_user)):
    if value not in (1,-1):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Value must be 1 (like) or -1(dislike)")
    
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")
    
    existing = db.query(Like).filter(Like.comment_id == comment_id, Like.user_id == current_user.id).first()

    if existing:
        existing.value = value
        db.commit()
        return {"detail": "Reaction updated", "value": value}
    
    new_like = Like(user_id = current_user.id, comment_id = comment_id, value = value)

    db.add(new_like)
    
    try:
        db.commint()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Reaction already exists (try again)")
    return {"detail": "Reaction added", "value": value}

@router.delete("/comment/{comment_id}", status_code=status.HTTP_200_OK)
def remove_reaction(comment_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    existing = db.query(Like).filter(Like.comment_id == comment_id, Like.user_id == current_user.id).first()

    if not existing:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reaction not found")
    
    db.delete(existing)
    db.commit()

    return {"detail": "Reaction removed"}