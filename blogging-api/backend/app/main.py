from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database.database import engine, Base
from app.models import user, post, comment, like  # noqa: F401 (needed to register models)

from app.routes.users import router as users_router
from app.routes.posts import router as posts_router
from app.routes.comments import router as comments_router
from app.routes.likes import router as likes_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Blogging API", version="0.1.0")

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],  # ✅ allows Authorization: Bearer <token>
)

app.include_router(users_router)
app.include_router(posts_router)
app.include_router(comments_router)
app.include_router(likes_router)

@app.get("/")
def root():
    return {"message": "Blogging API is running"}
