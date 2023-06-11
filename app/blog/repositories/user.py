from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from starlette import status

from app.blog import models
from app.blog.infra import schemas
from app.blog.services.hashing import Hash


def create(request: models.User, db: Session) -> schemas.User:
    new_user = schemas.User(name=request.name, email=request.email,
                            password=Hash.bcrypt(request.password),
                            secret=request.secret)
    db.add(new_user)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail=f'User with name {request.name} already exists')
    return new_user


def reset_password(request: models.User, db: Session) -> None:
    user = db.query(schemas.User).filter(schemas.User.email == request.email,
                                         schemas.User.name == request.name).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'User with the name {request.name} and email {request.email} is not found'
        )
    if not user.secret:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail='Impossible to recover user who did not configure secret'
        )
    else:
        if request.secret != user.secret:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail='Wrong secret'
            )
    user.password = Hash.bcrypt(request.password)
    db.add(user)
    db.commit()


def get_all(db: Session) -> list[schemas.User]:
    users = db.query(schemas.User).all()
    return users


def get_by_id(id: int, db: Session) -> schemas.User:
    user = db.query(schemas.User).filter(schemas.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'User with the id {id} is not found')
    return user


def delete(user_id: int, db: Session) -> str:
    user = db.query(schemas.User).filter(schemas.User.id == user_id)
    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'User with the id {user_id} is not found')
    user.delete()
    db.commit()
    return f'User with id {user_id} has been successfully deleted'
