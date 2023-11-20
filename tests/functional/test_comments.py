from fastapi.testclient import TestClient

from app.blog.infra.database import get_db
from app.blog.repositories import comment


def test_create_comment(test_client: TestClient) -> None:
    username = 'john'
    password = '123'
    blog_title = 'Cool title'
    comment_text = 'some text'

    with test_client:
        user_response = test_client.post(url='/users',
                                         json=dict(name=username,
                                                   password=password,
                                                   email='email@gmail.com'))

        assert user_response.status_code == 201

        auth_response = test_client.post(url='/login',
                                         data=dict(username=username,
                                                   password=password))

        assert auth_response.status_code == 200

        blog_response = test_client.post(
            url='/blogs', json=dict(title=blog_title, body='Some cool stuff'),
            headers={'Authorization': f'Bearer {auth_response.json()["access_token"]}'})

        assert blog_response.status_code == 201
        assert blog_response.json()['title'] == blog_title

        comments_response = test_client.post(
            url='/comments', json=dict(blog_title=blog_title, text=comment_text),
            headers={'Authorization': f'Bearer {auth_response.json()["access_token"]}'})

        assert comments_response.status_code == 201
        assert comments_response.json()['blog_title'] == blog_title
        assert comments_response.json()['text'] == comment_text


def test_delete_comment_success(test_client: TestClient) -> None:
    username = 'john'
    password = '123'
    blog_title = 'Cool title'
    comment_text = 'some text'

    with test_client:
        user_response = test_client.post(url='/users',
                                         json=dict(name=username,
                                                   password=password,
                                                   email='email@gmail.com'))

        assert user_response.status_code == 201

        auth_response = test_client.post(url='/login',
                                         data=dict(username=username,
                                                   password=password))

        assert auth_response.status_code == 200

        blog_response = test_client.post(
            url='/blogs', json=dict(title=blog_title, body='Some cool stuff'),
            headers={'Authorization': f'Bearer {auth_response.json()["access_token"]}'})

        assert blog_response.status_code == 201
        assert blog_response.json()['title'] == blog_title

        create_comments_response = test_client.post(
            url='/comments', json=dict(blog_title=blog_title, text=comment_text),
            headers={'Authorization': f'Bearer {auth_response.json()["access_token"]}'})

        assert create_comments_response.status_code == 201
        assert create_comments_response.json()['blog_title'] == blog_title
        assert create_comments_response.json()['text'] == comment_text

        db = next(get_db())

        created_comment_id = comment.get_id(blog_title, db)

        comments_response_delete = test_client.delete(
            url=f'/comments/{created_comment_id}',
            headers={'Authorization': f'Bearer {auth_response.json()["access_token"]}'})

        assert comments_response_delete.status_code == 200
        assert comments_response_delete.json() == \
            f'Comment with id {created_comment_id} has been successfully deleted'


def test_delete_comment_not_found(test_client: TestClient) -> None:
    username = 'john'
    password = '123'

    with test_client:
        user_response = test_client.post(url='/users',
                                         json=dict(name=username,
                                                   password=password,
                                                   email='email@gmail.com'))

        assert user_response.status_code == 201

        auth_response = test_client.post(url='/login',
                                         data=dict(username=username,
                                                   password=password))

        assert auth_response.status_code == 200

        comments_response_delete = test_client.delete(
            url=f'/comments/{0}',
            headers={'Authorization': f'Bearer {auth_response.json()["access_token"]}'})

        assert comments_response_delete.status_code == 404
        assert comments_response_delete.json() == {'detail':
                                                   f'Comment with the id {0} is not found'}
