from app.blog import models, schemas
from app.blog.database import get_db
from app.blog.repository import comment


def test_create_comment() -> None:
    text = 'some text'
    blog_title = 'cool title'
    user_name = 'john39'
    db = next(get_db())
    new_comment = comment.create(models.Comment(
        text=text, blog_title=blog_title), user_name=user_name, db=db)
    assert type(new_comment) is schemas.Comment
    assert new_comment.text == text
    assert new_comment.blog_title == blog_title
    assert new_comment.user_name == user_name
