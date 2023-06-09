from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status

from app.blog import models
from app.blog.database import get_db
from app.blog.repositories import blog
from app.blog.schemas import User
from app.oauth2 import get_current_user

router = APIRouter(
    prefix='/blog',
    tags=['Blogs']
)


@router.post('/', status_code=status.HTTP_201_CREATED)
def create_blog(request: models.Blog, db: Session = Depends(get_db),
                current_user: User = Depends(get_current_user)) -> models.ShowBlog:
    return models.ShowBlog.from_orm(blog.create(request, current_user.id, db))


@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update_blog(blog_id: int, request: models.Blog, db: Session = Depends(get_db),
                current_user: User = Depends(get_current_user)) -> str:
    return blog.update(blog_id, request, current_user.id, db)


@router.delete('/{id}', status_code=status.HTTP_200_OK)
def delete(blog_id: int, db: Session = Depends(get_db),
           current_user: User = Depends(get_current_user)) -> str:
    return blog.delete(blog_id, current_user.id, db)


@router.get('/', response_model=list[models.ShowBlog], status_code=status.HTTP_200_OK)
def show_all_blogs(db: Session = Depends(get_db)) -> list[models.ShowBlog]:
    return [models.ShowBlog.from_orm(blog_db) for blog_db in blog.get_all(db)]


@router.get('/{id}', response_model=models.ShowBlog, status_code=status.HTTP_200_OK)
def show_blog_by_id(blog_id: int, db: Session = Depends(get_db),
                    current_user: User = Depends(get_current_user)) -> models.ShowBlog:
    return models.ShowBlog.from_orm(blog.get_by_blog_id(blog_id, current_user.id, db))
