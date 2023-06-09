import pytest
from fastapi import HTTPException

from app.blog import models, schemas
from app.blog.database import get_db
from app.blog.repository import comment
from app.tests.conftest import random_string


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


def test_delete_comment_success() -> None:
    db = next(get_db())
    new_comment = comment.create(models.Comment(
        text='another some text', blog_title='different title'), user_name='john39', db=db)
    assert new_comment.user_name
    response = comment.delete(new_comment.id, new_comment.user_name, db=db)
    assert response == f'Comment with id {new_comment.id} has been successfully deleted'


def test_delete_comment_raises() -> None:
    db = next(get_db())
    with pytest.raises(HTTPException):
        comment.delete(0, random_string(), db=db)
