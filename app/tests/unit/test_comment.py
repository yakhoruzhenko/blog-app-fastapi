import pytest
from fastapi import HTTPException

from app.blog import models
from app.blog.infra import schemas
from app.blog.infra.database import get_db
from app.blog.repositories import blog, comment, user
from app.tests.conftest import random_string


def test_create_comment() -> None:
    text = 'some text'
    db = next(get_db())
    new_user = user.create(models.User(name='john39', email='email', password='password'), db)
    new_blog = blog.create(models.Blog(title='Cool title', body='blog body'), new_user.id, db)
    new_comment = comment.create(models.Comment(
        text=text, blog_title=new_blog.title), user_name=new_user.name, db=db)
    next(get_db())

    assert type(new_comment) is schemas.Comment
    assert new_comment.text == text
    assert new_comment.blog_title == new_blog.title
    assert new_comment.user_name == new_user.name


def test_delete_comment_success() -> None:
    db = next(get_db())
    new_user = user.create(models.User(name='john39', email='email', password='password'), db)
    new_blog = blog.create(models.Blog(title='Cool title', body='blog body'), new_user.id, db)
    new_comment = comment.create(models.Comment(
        text='text', blog_title=new_blog.title), user_name=new_user.name, db=db)

    assert new_comment.user_name

    response = comment.delete(new_comment.id, db)
    next(get_db())

    assert response == f'Comment with id {new_comment.id} has been successfully deleted'


def test_delete_comment_raises() -> None:
    db = next(get_db())
    with pytest.raises(HTTPException):
        comment.delete(0, db)
    next(get_db())


def test_get_commment_id_not_found() -> None:
    db = next(get_db())
    with pytest.raises(HTTPException):
        comment.get_id(random_string(), db)
    next(get_db())
