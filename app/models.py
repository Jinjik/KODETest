import datetime

from sqlalchemy import Boolean, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy_utils import URLType

from database import Base


class User(Base):
    """User model

    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    post = relationship("Post", back_populates="owner")


class Post(Base):
    """Post model

    """
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    body = Column(String)
    url = Column(String)
    created_date = Column(DateTime, default=datetime.datetime.utcnow())
    likes = Column(Integer, default=0, nullable=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="post")
    media = relationship("Media", back_populates="post")


class Media(Base):
    """Model for save path to media

    """
    __tablename__ = "medias"

    id = Column(Integer, primary_key=True)
    url = Column(URLType)
    post_id = Column(Integer(), ForeignKey("posts.id"))

    post = relationship("Post", back_populates="media")


class Like(Base):
    """Like model

    """
    __tablename__ = "likes"

    id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
