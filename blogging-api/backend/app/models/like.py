from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint, CheckConstraint
from sqlalchemy.orm import relationship
from app.database.database import Base

class Like(Base):
    __tablename__ = "likes"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=True)
    comment_id = Column(Integer, ForeignKey("comments.id"), nullable=True)

    __table_args__ = (
        UniqueConstraint("user_id", "post_id", name="unique_user_post_like"),
        UniqueConstraint("user_id", "comment_id", name="unique_user_comment_like"),
        CheckConstraint(
            "(post_id IS NOT NULL AND comment_id IS NULL) OR (post_id IS NULL AND comment_id IS NOT NULL)",
            name="like_exactly_one_target",
        ),
    )

    user = relationship("User", back_populates="likes")
    post = relationship("Post", back_populates="likes")
    comment = relationship("Comment", back_populates="likes")
