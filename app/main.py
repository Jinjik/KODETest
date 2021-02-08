from datetime import timedelta
from typing import List

import uvicorn
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI, HTTPException, status, UploadFile, File
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from jose import JWTError, jwt

import models
import schemas
import crud

from database import SessionLocal, engine


models.Base.metadata.create_all(bind=engine)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
ACCESS_TOKEN_EXPIRE_MINUTES = 30

tags_metadata = [
    {
        "name": "users",
        "description": "Operations with users. The **login** logic is also here.",
    },
    {
        "name": "posts",
        "description": "Manage with posts. View posts, create post, edit post, delete post",
    },
]

app = FastAPI(
    title="KODE Test Task",
    openapi_tags=tags_metadata,
)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


async def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, crud.SECRET_KEY, algorithms=[crud.ALGORITHM])
        username: str = payload.get("sub")

        if username is None:
            raise credentials_exception

        token_data = username
    except JWTError:
        raise credentials_exception

    user = crud.get_user(db, username=token_data)

    if user is None:
        raise credentials_exception

    return user


@app.post("/token/", response_model=schemas.Token, tags=["users"])
async def login_for_access_token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = crud.authenticate_user(db, form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = crud.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}


@app.post('/users/', tags=["users"])
def create_user(
        user: schemas.UserCreate,
        db: Session = Depends(get_db)
):
    return crud.create_user(db, user=user)


# Post


@app.post('/posts/', tags=["posts"])
def create_post(
        title: str,
        body: str,
        url: str,
        media: List[UploadFile] = File(...),
        db: Session = Depends(get_db),
        current_user: models.User = Depends(get_current_user)
):
    save_post = ""

    if current_user:
        user_id = current_user.id

        save_post = crud.create_post(db, user_id=user_id, title=title, body=body, url=url, media=media)

    if save_post:
        json_save_post = jsonable_encoder(save_post)
        return JSONResponse(content=json_save_post)

    return "Create failed!"


@app.get("/posts/", tags=["posts"])
def post_list(db: Session = Depends(get_db)):
    posts = crud.post_list(db)
    json_post_list = jsonable_encoder(posts)

    return JSONResponse(content=json_post_list)


@app.get("/posts/{post_id}", tags=["posts"])
def post_detail(post_id: int, db: Session = Depends(get_db)):
    post = crud.get_post(db, post_id)
    json_post = jsonable_encoder(post)

    return JSONResponse(content=json_post)


@app.post("/posts/{post_id}", tags=["posts"])
def post_update(post_id: int, title: str = None, body: str = None, url: str = None,
                db: Session = Depends(get_db),
                current_user: models.User = Depends(get_current_user)):
    post = crud.get_post(db, post_id)
    updated_post = ""

    if current_user.username == post["owner"]:
        updated_post = crud.update_post(db, title=title, body=body, post_id=post_id, url=url)

    if updated_post:
        json_updated_post = jsonable_encoder(post)
        return JSONResponse(content=json_updated_post)

    return f"Update failed!"


@app.delete("/posts/{post_id}/", tags=["posts"])
def post_delete(post_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    post = crud.get_post(db, post_id)

    if current_user.username == post["owner"]:
        title = crud.delete_post(db, post_id)

        if title:
            return f"Post {title} deleted!"

    return "Delete failed!"


@app.post("/posts/{post_id}like/", tags=["posts"])
def post_like(post_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    post = ""

    if current_user:
        post = crud.like_post(db, post_id, current_user.id)

    if post:
        return post

    return "Вы не авторизированы и не можете оценить пост"
