from fastapi import APIRouter, Depends
from starlette import status
from sqlalchemy.orm import Session
from typing import List
from .. import schemas, database
from ..repository import user


router = APIRouter(
    prefix='/user',
    tags=['Users']
)
get_db = database.get_db


@router.post('/', response_model=schemas.ShowUser, status_code=status.HTTP_201_CREATED)
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    return user.create(request, db)


@router.get('/{id}', response_model=schemas.ShowUser, status_code=status.HTTP_200_OK)
def get_user(id: int, db: Session = Depends(get_db)):
    return user.get_by_id(id, db)


@router.get('/', response_model=List[schemas.ShowUser], status_code=status.HTTP_200_OK)
def all_users(db: Session = Depends(get_db)):
    return user.get_all(db)
