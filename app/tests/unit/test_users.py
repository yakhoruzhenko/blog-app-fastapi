from fastapi.testclient import TestClient
from pytest_mock import MockerFixture

from app.blog.models import ShowUser, User


def test_create_comment(test_client: TestClient, mocker: MockerFixture) -> None:
    username = 'john'
    email = 'email@gmail.com'
    password = '123'
    id = 1

    mock_user_create = mocker.patch('app.blog.controllers.users.user.create')
    mock_show_user = mocker.patch('app.blog.controllers.users.ShowUser').model_validate
    mock_show_user.return_value = ShowUser(
        id=id,
        name=username,
        email=email,
        blogs=[],
        comments=[]
    )

    with test_client:
        user_response = test_client.post(url='/users',
                                         json=dict(name=username,
                                                   password=password,
                                                   email=email))

        assert user_response.status_code == 201
        mock_show_user.assert_called_once()
        assert User(name=username, email=email, password=password, secret=None) == \
            mock_user_create.call_args[0][0]
        assert user_response.json()['id'] == id
        assert user_response.json()['name'] == username
        assert user_response.json()['email'] == email
        assert user_response.json()['blogs'] == []
        assert user_response.json()['comments'] == []
