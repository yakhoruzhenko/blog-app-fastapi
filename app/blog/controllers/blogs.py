from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status
from tests.profiler import profile_func

from app.blog import models
from app.blog.infra.database import get_db
from app.blog.infra.schemas import User
from app.blog.repositories import blog
from app.blog.services.oauth2 import get_current_user

router = APIRouter(
    prefix='/blogs',
    tags=['Blogs']
)


@router.post('/', status_code=status.HTTP_201_CREATED)
@profile_func
def create_blog(request: models.Blog, db: Session = Depends(get_db),
                current_user: User = Depends(get_current_user)) -> models.ShowBlog:
    return models.ShowBlog.model_validate(blog.create(request, current_user.id, db))


@router.put('/{id}', status_code=status.HTTP_200_OK)
def update_blog(id: int, request: models.Blog, db: Session = Depends(get_db),
                current_user: User = Depends(get_current_user)) -> str:
    return blog.update(id, request, current_user.id, db)


@router.delete('/{id}', status_code=status.HTTP_200_OK)
def delete(id: int, db: Session = Depends(get_db),
           current_user: User = Depends(get_current_user)) -> str:
    return blog.delete(id, current_user.id, db)


@router.get('/', response_model=list[models.ShowBlog], status_code=status.HTTP_200_OK)
def show_all_blogs(db: Session = Depends(get_db)) -> list[models.ShowBlog]:
    return [models.ShowBlog.model_validate(blog_db) for blog_db in blog.get_all(db)]


@router.get('/{id}', response_model=models.ShowBlog, status_code=status.HTTP_200_OK)
def show_blog_by_id(id: int, db: Session = Depends(get_db),
                    current_user: User = Depends(get_current_user)) -> models.ShowBlog:
    return models.ShowBlog.model_validate(blog.get_by_blog_id(id, current_user.id, db))
