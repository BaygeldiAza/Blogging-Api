from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.database.database import Base

class CommentLike(Base):
    __tablename__ = "comment_likes"

    id = Column(Integer, primary_key = True, index = True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable = False)
    comment_id = Column(Integer, ForeignKey("comments.id"), nullable = False)
    like = Column(Integer, nullable = False)

    user = relationship("User", back_populates="liked_comments")
    comment = relationship("Comment", back_populates="likes")