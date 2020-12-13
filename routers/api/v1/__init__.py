from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

import schemas
from dependencies import get_db, get_current_user
from models.blog import Blog
from models.user_info import UserInfo
from project.settings import ACCESS_TOKEN_EXPIRE_MINUTES
from project.utils import create_access_token

router = APIRouter()


@router.post("/user", response_model=schemas.UserInfo)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = UserInfo.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return UserInfo.create_user(db=db, user=user)


@router.post("/authenticate", response_model=schemas.Token)
def authenticate_user(user: schemas.UserAuthenticate, db: Session = Depends(get_db)):
    db_user = UserInfo.get_user_by_username(db, username=user.username)
    if db_user is None:
        raise HTTPException(status_code=400, detail="Username not existed")
    else:
        is_password_correct = UserInfo.check_username_password(db, user)
        if is_password_correct is False:
            raise HTTPException(status_code=400, detail="Password is not correct")
        else:
            from datetime import timedelta

            access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

            access_token = create_access_token(
                data={"sub": user.username}, expires_delta=access_token_expires
            )
            return {"access_token": access_token, "token_type": "Bearer"}


@router.post("/blog", response_model=schemas.Blog)
async def create_new_blog(
    blog: schemas.BlogBase,
    current_user: UserInfo = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return Blog.create_new_blog(db=db, blog=blog)


@router.get("/blog")
async def get_all_blogs(
    current_user: UserInfo = Depends(get_current_user), db: Session = Depends(get_db)
):
    return Blog.get_all_blogs(db=db)


@router.get("/blog/{blog_id}")
async def get_blog_by_id(
    blog_id,
    current_user: UserInfo = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return Blog.get_blog_by_id(db=db, blog_id=blog_id)
