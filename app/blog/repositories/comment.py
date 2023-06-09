from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette import status

from app.blog import models, schemas


def create(request: models.Comment, user_name: str, db: Session) -> schemas.Comment:
    new_comment = schemas.Comment(text=request.text, blog_title=request.blog_title,
                                  user_name=user_name)
    db.add(new_comment)
    db.commit()
    return new_comment


def delete(comment_id: int, user_name: str, db: Session) -> str:
    selected_blog = db.query(schemas.Comment).filter(schemas.Comment.id == comment_id,
                                                     schemas.Comment.user_name == user_name)
    if not selected_blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Comment with the id {comment_id} is not found')
    selected_blog.delete()
    db.commit()
    return f'Comment with id {comment_id} has been successfully deleted'
