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


@router.put('/', status_code=status.HTTP_204_NO_CONTENT)
def update_user_password(request: User, db: Session = Depends(get_db)) -> None:
    user.reset_password(request, db)
