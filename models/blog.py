from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Session

import schemas
from project.database import Base


class Blog(Base):
    __tablename__ = "blog"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    content = Column(String)

    @classmethod
    def create_new_blog(cls, db: Session, blog: schemas.BlogBase):
        db_blog = cls(title=blog.title, content=blog.content)
        db.add(db_blog)
        db.commit()
        db.refresh(db_blog)
        return db_blog

    @classmethod
    def get_all_blogs(cls, db: Session):
        return db.query(cls).all()

    @classmethod
    def get_blog_by_id(cls, db: Session, blog_id: int):
        return db.query(cls).filter(cls.id == blog_id).first()
