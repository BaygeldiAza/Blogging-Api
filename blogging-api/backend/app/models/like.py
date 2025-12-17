from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.database.database import Base

class Like(Base):
    __tablename__ = "likes"

    id = Column(Integer, primary_key = True, index = True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable = False)
    comment_id = Column(Integer, ForeignKey("comments.id"), nullable = False)
    value = Column(Integer, nullable = False)

    user = relationship("User", back_populates="liked_comments")
    comment = relationship("Comment", back_populates="likes")

    __table_args__ = (UniqueConstraint("user_id", "comment_id", name = "unique_user_comment_like"))

