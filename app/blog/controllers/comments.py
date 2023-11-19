from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status

from app.blog import models
from app.blog.infra.database import get_db
from app.blog.infra.schemas import User
from app.blog.repositories import comment
from app.blog.services.oauth2 import get_current_user

router = APIRouter(
    prefix='/comments',
    tags=['Comments']
)


@router.post('/', status_code=status.HTTP_201_CREATED)
def create_comment(request: models.Comment, db: Session = Depends(get_db),
                   current_user: User = Depends(get_current_user)) -> models.ShowComment:
    return models.ShowComment.model_validate(comment.create(request, current_user.name, db))


@router.delete('/{id}', status_code=status.HTTP_200_OK)
def delete(id: int, db: Session = Depends(get_db),
           current_user: User = Depends(get_current_user)) -> str:
    return comment.delete(id, db)
