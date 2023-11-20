from fastapi.testclient import TestClient


def test_login_user_not_found(test_client: TestClient) -> None:
    username = 'john'

    with test_client:
        auth_response = test_client.post(url='/login',
                                         data=dict(username=username,
                                                   password='123'))

        assert auth_response.status_code == 404
        assert auth_response.json() == \
            {'detail': f'There is no username with such name: {username}'}


def test_login_hash_raises(test_client: TestClient) -> None:
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
                                                   password=password + '1'))

        assert auth_response.status_code == 401
        assert auth_response.json() == {'detail': f'Invalid password for {username}'}
