import shutil
from datetime import datetime, timedelta
from typing import Optional, List

from fastapi import UploadFile
from sqlalchemy.orm import Session
from jose import jwt
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer

import models
import schemas

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Register


def verify_password(plain_password, hashed_password) -> CryptContext:
    """Function for verify password

    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password) -> CryptContext:
    """Function for hash password

    """
    return pwd_context.hash(password)


def get_user(db: Session, username: str):
    """Function for get user

    """
    return db.query(models.User).filter(models.User.username == username).first()


def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    """ Function for create user

    """
    db_user = models.User(username=user.username, hashed_password=get_password_hash(user.password))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def authenticate_user(fake_db, username: str, password: str):
    """Function for authenticate user

    """
    user = get_user(fake_db, username)

    if not user:
        return False

    if not verify_password(password, user.hashed_password):
        return False

    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create access token for user

    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


# Posts

def save_media(db: Session, post_id, media):
    """ Function for save media

    """
    for file in media:

        with open(f'media/{file.filename}', 'wb') as image:
            shutil.copyfileobj(file.file, image)
            db_media = models.Media(url=str(f'media/{file.filename}'), post_id=post_id)
            db.add(db_media)

        db.commit()


def create_post(db: Session, user_id: int, title: str, body: str, url: str, media: List[UploadFile]):
    """ Function for create post

    """
    db_post = models.Post(title=title, body=body, owner_id=user_id, url=url)
    db.add(db_post)
    db.commit()

    save_media(db, db_post.id, media)

    print(db_post.media)

    return db_post


def update_post(db: Session, title: str, body: str, url: str, post_id: int):
    """ Function for update post

    """
    post = db.query(models.Post).filter(models.Post.id == post_id).first()

    if title:
        post.title = title

    if body:
        post.body = body

    if url:
        post.url = url

    db.add(post)
    db.commit()

    return post


def delete_post(db: Session, post_id: int):
    """Function for delete post

    """
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    title = post.title
    db.delete(post)
    db.commit()

    return title


def get_post(db: Session, post_id: int):
    """Function for get user

    """
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    response = {
        "id": post.id,
        "title": post.title,
        "body": post.body,
        "url": post.url,
        "media": post.media,
        "owner": post.owner.username,
        "created_date": post.created_date
    }
    return response


def post_list(db: Session):
    """Function for get user

    """
    posts = db.query(models.Post).all()
    response = []

    for post in posts:
        response.append({
            "id": post.id,
            "title": post.title,
            "body": post.body,
            "url": post.url,
            "media": post.media,
            "owner": post.owner.username,
            "created_date": post.created_date
        })

    return response


def like_post(db: Session, post_id: int, user_id: int):
    """Function for like post

    """
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    like = db.query(models.Like).filter(models.Like.post_id == post_id).first()

    if like is None:
        like = models.Like(post_id=post_id, user_id=user_id)
        post.likes = post.likes + 1
        db.add(like)
    else:
        post.likes = post.likes - 1
        db.delete(like)

    db.add(post)
    db.commit()

    return post
