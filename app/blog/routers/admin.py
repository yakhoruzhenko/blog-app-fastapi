from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status

from app.blog.database import get_db
from app.blog.models import ShowUser
from app.blog.repository import user
from app.oauth2 import fake_admin_token

router = APIRouter(
    prefix='/admin/user',
    tags=['Admin']
)


@router.get('/{id}', response_model=ShowUser, status_code=status.HTTP_200_OK)
def get_user_by_id(id: int, db: Session = Depends(get_db),
                   fake_valitaton: None = Depends(fake_admin_token)) -> ShowUser:
    return ShowUser.from_orm(user.get_by_id(id, db))


@router.get('/', response_model=list[ShowUser], status_code=status.HTTP_200_OK)
def all_users(db: Session = Depends(get_db),
              fake_valitaton: None = Depends(fake_admin_token)) -> list[ShowUser]:
    return [ShowUser.from_orm(user_db) for user_db in user.get_all(db)]


@router.delete('/{id}', status_code=status.HTTP_200_OK)
def delete_by_user_id(id: int, db: Session = Depends(get_db),
                      fake_valitaton: None = Depends(fake_admin_token)) -> str:
    return user.delete(id, db)
