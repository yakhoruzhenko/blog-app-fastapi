from fastapi.testclient import TestClient
from tests.conftest import random_string


def test_create_user_already_exists(test_client: TestClient) -> None:
    username = 'john'
    password = '123'

    with test_client:
        first_user_response = test_client.post(url='/users',
                                               json=dict(name=username,
                                                         password=password,
                                                         email='email@gmail.com'))

        assert first_user_response.status_code == 201

        second_user_response = test_client.post(url='/users',
                                                json=dict(name=username,
                                                          password=password + '1',
                                                          email='mymail@gmail.com'))

        assert second_user_response.status_code == 422
        assert second_user_response.json() == \
            {'detail': f'User with name {username} already exists'}


def test_update_user_password_success(test_client: TestClient) -> None:
    username = 'john'
    password = '123'
    new_password = '321'
    secret = '123'

    with test_client:
        create_user_response = test_client.post(url='/users',
                                                json=dict(name=username,
                                                          password=password,
                                                          email='email@gmail.com',
                                                          secret=secret))

        assert create_user_response.status_code == 201

        update_password_response = test_client.put(url='/users',
                                                   json=dict(name=username,
                                                             password=new_password,
                                                             email='email@gmail.com',
                                                             secret=secret))

        assert update_password_response.status_code == 204
        assert update_password_response.text == ''


def test_update_user_password_no_secret_set(test_client: TestClient) -> None:
    username = 'john'
    password = '123'
    new_password = '321'

    with test_client:
        create_user_response = test_client.post(url='/users',
                                                json=dict(name=username,
                                                          password=password,
                                                          email='email@gmail.com'))

        assert create_user_response.status_code == 201

        update_password_response = test_client.put(url='/users',
                                                   json=dict(name=username,
                                                             password=new_password,
                                                             email='email@gmail.com'))

        assert update_password_response.status_code == 422
        assert update_password_response.json() == \
            {'detail': 'Impossible to recover user who did not configure secret'}


def test_update_user_password_secrets_dont_match(test_client: TestClient) -> None:
    username = 'john'
    password = '123'
    new_password = '321'
    secret = '123'
    new_secret = '321'

    with test_client:
        create_user_response = test_client.post(url='/users',
                                                json=dict(name=username,
                                                          password=password,
                                                          email='email@gmail.com',
                                                          secret=secret))

        assert create_user_response.status_code == 201

        update_password_response = test_client.put(url='/users',
                                                   json=dict(name=username,
                                                             password=new_password,
                                                             email='email@gmail.com',
                                                             secret=new_secret))

        assert update_password_response.status_code == 403
        assert update_password_response.json() == {'detail': 'Wrong secret'}


def test_update_user_password_user_missing(test_client: TestClient) -> None:
    with test_client:
        name = random_string()
        email = random_string()
        update_password_response = test_client.put(url='/users',
                                                   json=dict(name=name,
                                                             password='111',
                                                             email=email,
                                                             secret='secret'))

        assert update_password_response.status_code == 404
        assert update_password_response.json() == \
            {'detail': f'User with the name {name} and email {email} is not found'}


def test_get_current_user_profile(test_client: TestClient) -> None:
    username = 'john'
    password = '123'

    with test_client:
        create_user_response = test_client.post(url='/users',
                                                json=dict(name=username,
                                                          password=password,
                                                          email='email@gmail.com'))

        assert create_user_response.status_code == 201

        auth_response = test_client.post(url='/login',
                                         data=dict(username=username,
                                                   password=password))

        assert auth_response.status_code == 200

        get_user_profile_response = test_client.get(
            url='/users',
            headers={'Authorization': f'Bearer {auth_response.json()["access_token"]}'})

        assert get_user_profile_response.status_code == 200
        assert get_user_profile_response.json() == create_user_response.json()
