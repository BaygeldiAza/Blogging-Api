from fastapi import FastAPI
from app.database.database import engine, Base
from app.models import user, post, comment
from app.routes import users, posts, comments

Base.metadata.create_all(bind = engine)

app = FastAPI(
    title="Blogging API",
    version="0.1.0",
)

app.include_router(users.router)
app.include_router(posts.router)
app.include_router(comments.router)