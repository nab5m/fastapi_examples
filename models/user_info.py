import bcrypt
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Session

import schemas
from project.database import Base


class UserInfo(Base):
    __tablename__ = "user_info"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    password = Column(String)
    fullname = Column(String, unique=True)

    @classmethod
    def get_user_by_username(cls, db: Session, username: str):
        return db.query(cls).filter(cls.username == username).first()

    @classmethod
    def create_user(cls, db: Session, user: schemas.UserCreate):
        hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
        db_user = cls(username=user.username, password=hashed_password, fullname=user.fullname)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    @classmethod
    def check_username_password(cls, db: Session, user: schemas.UserAuthenticate):
        db_user_info: cls = cls.get_user_by_username(db, username=user.username)
        return bcrypt.checkpw(user.password.encode('utf-8'), db_user_info.password.encode('utf-8'))
