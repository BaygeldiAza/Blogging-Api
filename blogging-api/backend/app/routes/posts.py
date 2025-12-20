from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database.database import get_db
from app.dependencies.auth import get_current_user
from app.models.post import Post
from app.models.comment import Comment
from app.models.like import Like
from app.models.user import User
from app.schemas.post import PostCreate, PostOut

router = APIRouter(prefix="/posts", tags=["Posts"])

@router.post("/", response_model=PostOut, status_code=status.HTTP_201_CREATED)
def create_post(
    post_in: PostCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    new_post = Post(
        title=post_in.title,
        content=post_in.content,
        author_id=current_user.id,
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    # computed fields
    new_post.author_username = current_user.username
    new_post.comment_count = 0
    new_post.like_count = 0
    new_post.dislike_count = 0
    new_post.liked_by_me = False
    new_post.likes_count = 0
    new_post.comments_count = 0

    return new_post

@router.get("/", response_model=List[PostOut])
def list_posts(db: Session = Depends(get_db), limit: int = 20, skip: int = 0):
    posts = (
        db.query(Post)
        .order_by(Post.id.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    if not posts:
        return []

    post_ids = [p.id for p in posts]

    comment_counts = dict(
        db.query(Comment.post_id, func.count(Comment.id))
        .filter(Comment.post_id.in_(post_ids))
        .group_by(Comment.post_id)
        .all()
    )

    like_counts = dict(
        db.query(Like.post_id, func.count(Like.id))
        .filter(Like.post_id.in_(post_ids))
        .group_by(Like.post_id)
        .all()
    )

    for p in posts:
        p.author_username = p.author.username
        p.comment_count = int(comment_counts.get(p.id, 0))
        p.like_count = int(like_counts.get(p.id, 0))
        p.dislike_count = 0
        p.liked_by_me = False
        p.likes_count = p.like_count
        p.comments_count = p.comment_count

    return posts

@router.get("/{post_id}", response_model=PostOut)
def get_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    post.author_username = post.author.username
    post.comment_count = db.query(Comment).filter(Comment.post_id == post_id).count()
    post.like_count = db.query(Like).filter(Like.post_id == post_id).count()
    post.dislike_count = 0
    post.liked_by_me = False
    post.likes_count = post.like_count
    post.comments_count = post.comment_count

    return post

@router.put("/{post_id}", response_model=PostOut)
def update_post(
    post_id: int,
    post_in: PostCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    if post.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not allowed")

    post.title = post_in.title
    post.content = post_in.content
    db.commit()
    db.refresh(post)

    post.author_username = post.author.username
    post.comment_count = db.query(Comment).filter(Comment.post_id == post_id).count()
    post.like_count = db.query(Like).filter(Like.post_id == post_id).count()
    post.dislike_count = 0
    post.liked_by_me = False
    post.likes_count = post.like_count
    post.comments_count = post.comment_count

    return post

@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    if post.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not allowed")

    db.delete(post)
    db.commit()
    return None
