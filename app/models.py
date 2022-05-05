from turtle import title
from sqlalchemy import TIMESTAMP, Column, ForeignKey, Integer, String, UniqueConstraint, text
from sqlalchemy.orm import relationship
from .database import Base

# SqlAlchemy Models

class PostModel(Base):
    __tablename__ = "posts"

    # Columns
    id = Column(Integer, primary_key = True, nullable = False)
    title = Column(String, nullable = False)
    content = Column(String, nullable = False)
    published_at = Column(TIMESTAMP(timezone = True), nullable = False, server_default = text('now()'))
    owner_id = Column(Integer, ForeignKey("users.id", ondelete= "CASCADE"), nullable = False)

    owner = relationship("User")

class User(Base):
    __tablename__ = "users"

    # Columns
    id = Column(Integer, primary_key = True, nullable = False)
    email = Column(String, nullable = False, unique = True)
    password = Column(String, nullable = False)
    created_at = Column(TIMESTAMP(timezone = True), nullable = False, server_default = text('now()'))

class Vote(Base):
    __tablename__ = "votes"

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key= True)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key= True)