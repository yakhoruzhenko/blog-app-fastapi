from fastapi import APIRouter, Depends
from starlette import status
from typing import List
from sqlalchemy.orm import Session
from .. import schemas, database
from ..repository import blog
import oauth2

router = APIRouter(
    prefix='/blog',
    tags=['Blogs']
)
get_db = database.get_db


@router.post('/', status_code=status.HTTP_201_CREATED)
def create_blog(request: schemas.Blog, db: Session = Depends(get_db),
                current_user: schemas.User = Depends(oauth2.get_current_user)):
    return blog.create(request, db)


@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update_blog(task_id: int, request: schemas.Blog, db: Session = Depends(get_db),
                current_user: schemas.User = Depends(oauth2.get_current_user)):
    return blog.update(task_id, request, db)


@router.delete('/{id}')
def delete(task_id: int, db: Session = Depends(get_db),
           current_user: schemas.User = Depends(oauth2.get_current_user)):
    return blog.delete(task_id, db)


@router.get('/', response_model=List[schemas.ShowBlog], status_code=status.HTTP_200_OK)
def show_all_blogs(db: Session = Depends(get_db),
                   current_user: schemas.User = Depends(oauth2.get_current_user)):
    return blog.get_all(db)


@router.get('/{id}', response_model=schemas.ShowBlog, status_code=status.HTTP_200_OK)
def show_blog_by_id(task_id: int, db: Session = Depends(get_db),
                    current_user: schemas.User = Depends(oauth2.get_current_user)):
    return blog.get_by_id(task_id, db)
