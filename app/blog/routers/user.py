from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status

from app.blog.database import get_db
from app.blog.models import ShowUser, User
from app.blog.repository import user

router = APIRouter(
    prefix='/user',
    tags=['Users']
)


@router.post('/', response_model=ShowUser, status_code=status.HTTP_201_CREATED)
def create_user(request: User, db: Session = Depends(get_db)) -> ShowUser:
    return ShowUser.from_orm(user.create(request, db))


@router.get('/{id}', response_model=ShowUser, status_code=status.HTTP_200_OK)
def get_user_by_blog_id(id: int, db: Session = Depends(get_db)) -> ShowUser:
    return ShowUser.from_orm(user.get_by_blog_id(id, db))


@router.get('/', response_model=list[ShowUser], status_code=status.HTTP_200_OK)
def all_users(db: Session = Depends(get_db)) -> list[ShowUser]:
    return [ShowUser.from_orm(user_db) for user_db in user.get_all(db)]


@router.delete('/{id}', status_code=status.HTTP_200_OK)
def delete_by_user_id(id: int, db: Session = Depends(get_db)) -> str:
    return user.delete(id, db)
