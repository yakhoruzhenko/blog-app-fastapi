from sqlalchemy.orm import Session

from app.blog import models, schemas


def create(request: models.Comment, user_name: str, db: Session) -> schemas.Comment:
    new_comment = schemas.Comment(text=request.text, blog_title=request.blog_title,
                                  user_name=user_name)
    db.add(new_comment)
    db.commit()
    return new_comment
