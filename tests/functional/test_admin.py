from fastapi.testclient import TestClient
from tests.conftest import random_string


def test_get_user_by_id_success(test_client: TestClient) -> None:
    with test_client:
        create_user_response = test_client.post(url='/users',
                                                json=dict(name='john',
                                                          password='123',
                                                          email='email@gmail.com'))

        assert create_user_response.status_code == 201

        get_user_response = test_client.get(
            url=f'/admin/user/{create_user_response.json()["id"]}',
            headers={'token': 'admin_token'})

        assert get_user_response.status_code == 200
        assert get_user_response.json() == create_user_response.json()


def test_get_user_by_id_success_wrong_token(test_client: TestClient) -> None:
    with test_client:
        create_user_response = test_client.post(url='/users',
                                                json=dict(name='john',
                                                          password='123',
                                                          email='email@gmail.com'))

        assert create_user_response.status_code == 201

        get_user_response = test_client.get(
            url=f'/admin/user/{create_user_response.json()["id"]}',
            headers={'token': random_string()})

        assert get_user_response.status_code == 401
        assert get_user_response.json() == {'detail': 'Invalid admin token'}


def test_get_user_by_id_not_found(test_client: TestClient) -> None:
    id = 0
    with test_client:
        get_user_response = test_client.get(
            url=f'/admin/user/{id}',
            headers={'token': 'admin_token'})

        assert get_user_response.status_code == 404
        assert get_user_response.json() == {'detail': f'User with the id {id} is not found'}


def test_get_all_users(test_client: TestClient) -> None:
    with test_client:
        get_user_response = test_client.get(
            url='/admin/user/',
            headers={'token': 'admin_token'})

        assert get_user_response.status_code == 200
        assert get_user_response.json() == []


def test_delete_user_by_id_success(test_client: TestClient) -> None:
    username = 'john'
    password = '123'
    blog_title = 'test title'
    comment_text = 'test comment'

    with test_client:
        create_user_response = test_client.post(url='/users',
                                                json=dict(name=username,
                                                          password='123',
                                                          email='email@gmail.com'))

        assert create_user_response.status_code == 201

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

        show_blog_response = test_client.get(
            url=f'/blogs/{blog_response.json()["id"]}',
            headers={'Authorization': f'Bearer {auth_response.json()["access_token"]}'})

        assert show_blog_response.status_code == 200
        assert show_blog_response.json() != blog_response.json()
        updated_blog_response = blog_response.json()
        updated_blog_response['comments'].append(comments_response.json())
        assert show_blog_response.json() == updated_blog_response

        delete_user_response = test_client.delete(
            url=f'/admin/user/{create_user_response.json()["id"]}',
            headers={'token': 'admin_token'})

        assert delete_user_response.status_code == 200
        assert delete_user_response.json() == \
            f'User with id {create_user_response.json()["id"]} has been successfully deleted'

        get_user_response = test_client.get(
            url=f'/admin/user/{create_user_response.json()["id"]}',
            headers={'token': 'admin_token'})

        assert get_user_response.status_code == 404

        show_blog_response = test_client.get(
            url=f'/blogs/{blog_response.json()["id"]}',
            headers={'Authorization': f'Bearer {auth_response.json()["access_token"]}'})

        assert show_blog_response.status_code == 404


def test_delete_user_by_id_not_found(test_client: TestClient) -> None:
    id = 0
    delete_user_response = test_client.delete(
        url=f'/admin/user/{id}',
        headers={'token': 'admin_token'})

    assert delete_user_response.status_code == 404
    assert delete_user_response.json() == {'detail': f'User with the id {id} is not found'}
