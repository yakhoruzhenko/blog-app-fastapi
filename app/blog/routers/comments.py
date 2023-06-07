from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status

from app.blog import models
from app.blog.database import get_db
from app.blog.repository import comment
from app.blog.schemas import User
from app.oauth2 import get_current_user

router = APIRouter(
    prefix='/comments',
    tags=['Comments']
)


@router.post('/', status_code=status.HTTP_201_CREATED)
def create_comment(request: models.Comment, db: Session = Depends(get_db),
                   current_user: User = Depends(get_current_user)) -> models.ShowComment:
    return models.ShowComment.from_orm(comment.create(request, current_user.name, db))
