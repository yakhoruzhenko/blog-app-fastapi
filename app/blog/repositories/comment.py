from typing import cast

from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette import status

from app.blog import models
from app.blog.infra import schemas


def create(request: models.Comment, user_name: str, db: Session) -> schemas.Comment:
    new_comment = schemas.Comment(text=request.text, blog_title=request.blog_title,
                                  user_name=user_name)
    db.add(new_comment)
    db.commit()
    return new_comment


def delete(comment_id: int, db: Session) -> str:
    selected_comment = db.query(schemas.Comment).filter(schemas.Comment.id == comment_id)
    if not selected_comment.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Comment with the id {comment_id} is not found')
    selected_comment.delete()
    db.commit()
    return f'Comment with id {comment_id} has been successfully deleted'


def get_id(blog_title: str, db: Session) -> int:
    selected_comment = db.query(schemas.Comment).filter(schemas.Comment.blog_title == blog_title)
    if not selected_comment.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Comment with the blog_title {blog_title} is not found')
    return cast(int, selected_comment.scalar().id)
