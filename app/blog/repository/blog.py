from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette import status

from app.blog import models, schemas


def create(request: models.Blog, user_id: int, db: Session) -> schemas.Blog:
    new_blog = schemas.Blog(title=request.title, body=request.body, user_id=user_id)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


def get_all(user_id: int, db: Session) -> list[schemas.Blog]:
    blogs = db.query(schemas.Blog).filter(schemas.Blog.user_id == user_id).all()
    return blogs


def get_by_blog_id(blog_id: int, user_id: int, db: Session) -> schemas.Blog:
    selected_blog = db.query(schemas.Blog).filter(schemas.Blog.id == blog_id,
                                                  schemas.Blog.user_id == user_id).first()
    if not selected_blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Blog with the id {blog_id} is not found')
    return selected_blog


def update(blog_id: int, request: models.Blog, user_id: int, db: Session) -> str:
    selected_blog = db.query(schemas.Blog).filter(schemas.Blog.id == blog_id,
                                                  schemas.Blog.user_id == user_id)
    if not selected_blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Blog with the id {blog_id} is not found')
    selected_blog.update({'title': request.title, 'body': request.body})
    db.commit()
    return f'Blog with id {blog_id} has been successfully updated'


def delete(blog_id: int, user_id: int, db: Session) -> str:
    selected_blog = db.query(schemas.Blog).filter(schemas.Blog.id == blog_id,
                                                  schemas.Blog.user_id == user_id)
    if not selected_blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Blog with the id {blog_id} is not found')
    selected_blog.delete()
    db.commit()
    return f'Blog with id {blog_id} has been successfully deleted'
