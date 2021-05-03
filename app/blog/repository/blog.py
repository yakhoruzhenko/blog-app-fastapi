from sqlalchemy.orm import Session
from fastapi import HTTPException
from starlette import status
from blog import schemas, models


def create(request: schemas.Blog, db):
    new_blog = models.Blog(title=request.title, body=request.body, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


def get_all(db: Session):
    blogs = db.query(models.Blog).all()
    return blogs


def get_by_id(task_id: int, db: Session):
    selected_blog = db.query(models.Blog).filter(models.Blog.id == task_id).first()
    if not selected_blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Blog with the id {task_id} is not found')
    return selected_blog


def update(task_id: int, request: schemas.Blog, db):
    selected_blog = db.query(models.Blog).filter(models.Blog.id == task_id)
    if not selected_blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Blog with the id {task_id} is not found')
    selected_blog.update({'title': request.title, 'body': request.body}, synchronize_session=False)
    db.commit()
    return f'Blog with id {task_id} has been successfully updated'


def delete(task_id: int, db: Session):
    selected_blog = db.query(models.Blog).filter(models.Blog.id == task_id)
    if not selected_blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Blog with the id {task_id} is not found')
    selected_blog.delete(synchronize_session=False)
    db.commit()
    return f'Blog with id {task_id} has been successfully deleted'
