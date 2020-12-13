from datetime import timedelta, datetime

import jwt

from project.settings import JWT_SECRET_KEY, JWT_ALGORITHM


def create_access_token(*, data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return encoded_jwt


def decode_access_token(*, data: str):
    to_decode = data
    return jwt.decode(to_decode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
