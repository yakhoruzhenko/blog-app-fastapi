from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status

from app.blog.infra.database import get_db
from app.blog.infra.schemas import User as UserDB
from app.blog.models import ShowUser, User
from app.blog.repositories import user
from app.blog.services.oauth2 import get_current_user

router = APIRouter(
    prefix='/users',
    tags=['Users']
)


@router.post('/', response_model=ShowUser, status_code=status.HTTP_201_CREATED)
def create_user(request: User, db: Session = Depends(get_db)) -> ShowUser:
    return ShowUser.model_validate(user.create(request, db))


@router.put('/', status_code=status.HTTP_204_NO_CONTENT)
def update_user_password(request: User, db: Session = Depends(get_db)) -> None:
    user.reset_password(request, db)


@router.get('/', response_model=ShowUser, status_code=status.HTTP_200_OK)
def get_current_user_profile(db: Session = Depends(get_db),
                             current_user: UserDB = Depends(get_current_user)) -> ShowUser:
    return ShowUser.model_validate(user.get_by_id(current_user.id, db))
