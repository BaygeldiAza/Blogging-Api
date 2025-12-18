from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session 
from sqlalchemy import func, case
from app.schemas.post import PostOut, PostCreate 
from app.models.post import Post
from app.models.comment import Comment
from app.models.like import Like
from app.database.database import get_db
from app.dependencies.auth import get_current_user

router = APIRouter(prefix="/posts", tags=["Posts"])

@router.post("/",response_model=PostOut, status_code=status.HTTP_201_CREATED)
def create_post(post_in: PostCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    #This route is protected: Only logged in users can post 
    new_post = Post(title = post_in.title, 
                    content = post_in.content,
                    author_id = current_user.id,
    )

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post

@router.get("/", response_model=List[PostOut])
def list_posts(db: Session = Depends(get_db), sort: str = "newest", limit: int = 10, skip: int = 0):
    posts = (db.query(Post).order_by(Post.id.desc()).offset(skip).limit(limit).all())

    if not posts:
        return []
    
    post_ids = [p.id for p in posts]

    comment_counts = (
        db.query(Comment.post_id, func.count(Comment.id))
        .filter(Comment.post_id.in_(post_ids))
        .group_by(Comment.post_id)
        .all()
    )
    comment_map = {pid: int(cnt) for pid, cnt in comment_counts}

     # like/dislike counts per post (from comment reactions)
    reaction_counts = (
        db.query(
            Comment.post_id.label("post_id"),
            func.sum(case((Like.value == 1, 1), else_=0)).label("like_count"),
            func.sum(case((Like.value == -1, 1), else_=0)).label("dislike_count"),
        )
        .join(Comment, Comment.id == Like.comment_id)
        .filter(Comment.post_id.in_(post_ids))
        .group_by(Comment.post_id)
        .all()
    )

    reaction_map = {
        row.post_id: (int(row.like_count or 0), int(row.dislike_count or 0))
        for row in reaction_counts
    }

    # attach extra fields
    for post in posts:
        post.comment_count = comment_map.get(post.id, 0)
        like_count, dislike_count = reaction_map.get(post.id, (0, 0))
        post.like_count = like_count
        post.dislike_count = dislike_count

    # sorting
    if sort == "top":
        posts.sort(key=lambda p: p.like_count, reverse=True)
    else:
        posts.sort(key=lambda p: p.id, reverse=True)

    return posts