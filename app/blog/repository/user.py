from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette import status

from app.blog import models, schemas
from app.hashing import Hash


def create(request: models.User, db: Session) -> schemas.User:
    new_user = schemas.User(name=request.name, email=request.email,
                            password=Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_all(db: Session) -> list[schemas.User]:
    users = db.query(schemas.User).all()
    return users


def get_by_blog_id(blog_id: int, db: Session) -> schemas.User:
    user = db.query(schemas.User).filter(schemas.User.blogs.id == blog_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'User with the id {blog_id} is not found')
    return user


def delete(user_id: int, db: Session) -> str:
    user = db.query(schemas.User).filter(schemas.User.id == user_id)
    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'User with the id {user_id} is not found')
    user.delete()
    db.commit()
    return f'User with id {user_id} has been successfully deleted'
