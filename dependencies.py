from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from jwt import PyJWTError
from sqlalchemy.orm import Session
from starlette import status

from project.database import SessionLocal
from project.utils import decode_access_token
from schemas.token import TokenData
from models.user_info import UserInfo


def get_db():
    db = None
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/authenticate")


async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_access_token(data=token)
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except PyJWTError:
        raise credentials_exception
    user = UserInfo.get_user_by_username(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user
