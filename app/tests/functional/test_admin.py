from fastapi.testclient import TestClient

from app.tests.conftest import random_string


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
    with test_client:
        create_user_response = test_client.post(url='/users',
                                                json=dict(name='john',
                                                          password='123',
                                                          email='email@gmail.com'))

        assert create_user_response.status_code == 201

        get_user_response = test_client.delete(
            url=f'/admin/user/{create_user_response.json()["id"]}',
            headers={'token': 'admin_token'})

        assert get_user_response.status_code == 200
        assert get_user_response.json() == \
            f'User with id {create_user_response.json()["id"]} has been successfully deleted'


def test_delete_user_by_id_not_found(test_client: TestClient) -> None:
    id = 0
    get_user_response = test_client.delete(
        url=f'/admin/user/{id}',
        headers={'token': 'admin_token'})

    assert get_user_response.status_code == 404
    assert get_user_response.json() == {'detail': f'User with the id {id} is not found'}
