from fastapi.testclient import TestClient


def test_create_blog_already_exists(test_client: TestClient) -> None:
    username = 'john'
    password = '123'
    title = 'Cool title'

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

        first_blog_response = test_client.post(
            url='/blogs', json=dict(title=title, body='Some cool stuff'),
            headers={'Authorization': f'Bearer {auth_response.json()["access_token"]}'})

        assert first_blog_response.status_code == 201
        assert first_blog_response.json()['title'] == title

        second_blog_response = test_client.post(
            url='/blogs', json=dict(title=title, body='Some cool stuff'),
            headers={'Authorization': f'Bearer {auth_response.json()["access_token"]}'})

        assert second_blog_response.status_code == 422
        assert second_blog_response.json() == {'detail': f'Blog with title {title} already exists'}


def test_create_update_blog_success(test_client: TestClient) -> None:
    username = 'john'
    password = '123'
    title = 'Cool title'

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

        create_blog_response = test_client.post(
            url='/blogs', json=dict(title=title, body='Some cool stuff'),
            headers={'Authorization': f'Bearer {auth_response.json()["access_token"]}'})

        assert create_blog_response.status_code == 201
        assert create_blog_response.json()['title'] == title
        blog_id = create_blog_response.json()['id']

        update_blog_response = test_client.put(
            url=f'/blogs/{blog_id}', json=dict(title=title, body='New cool stuff'),
            headers={'Authorization': f'Bearer {auth_response.json()["access_token"]}'})

        assert update_blog_response.status_code == 200
        assert update_blog_response.json() == \
            f'Blog with id {blog_id} has been successfully updated'


def test_create_update_blog_not_found(test_client: TestClient) -> None:
    username = 'john'
    password = '123'
    title = 'Cool title'
    blog_id = 0

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

        update_blog_response = test_client.put(
            url=f'/blogs/{blog_id}', json=dict(title=title, body='New cool stuff'),
            headers={'Authorization': f'Bearer {auth_response.json()["access_token"]}'})

        assert update_blog_response.status_code == 404
        assert update_blog_response.json() == {'detail': f'Blog with the id {blog_id} is not found'}


def test_delete_blog_success(test_client: TestClient) -> None:
    username = 'john'
    password = '123'
    title = 'Cool title'

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

        create_blog_response = test_client.post(
            url='/blogs', json=dict(title=title, body='Some cool stuff'),
            headers={'Authorization': f'Bearer {auth_response.json()["access_token"]}'})

        assert create_blog_response.status_code == 201
        assert create_blog_response.json()['title'] == title
        blog_id = create_blog_response.json()['id']

        delete_blog_response = test_client.delete(
            url=f'/blogs/{blog_id}',
            headers={'Authorization': f'Bearer {auth_response.json()["access_token"]}'})

        assert delete_blog_response.status_code == 200
        assert delete_blog_response.json() == \
            f'Blog with id {blog_id} has been successfully deleted'


def test_delete_blog_not_found(test_client: TestClient) -> None:
    username = 'john'
    password = '123'
    blog_id = 0

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

        delete_blog_response = test_client.delete(
            url=f'/blogs/{blog_id}',
            headers={'Authorization': f'Bearer {auth_response.json()["access_token"]}'})

        assert delete_blog_response.status_code == 404
        assert delete_blog_response.json() == {'detail': f'Blog with the id {blog_id} is not found'}


def test_get_all_blogs(test_client: TestClient) -> None:
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

        get_all_blogs_response = test_client.get(
            url='/blogs/',
            headers={'Authorization': f'Bearer {auth_response.json()["access_token"]}'})

        assert get_all_blogs_response.status_code == 200
        assert get_all_blogs_response.json() == []


def test_show_blog_by_id_success(test_client: TestClient) -> None:
    username = 'john'
    password = '123'
    title = 'Cool title'

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

        create_blog_response = test_client.post(
            url='/blogs', json=dict(title=title, body='Some cool stuff'),
            headers={'Authorization': f'Bearer {auth_response.json()["access_token"]}'})

        assert create_blog_response.status_code == 201
        assert create_blog_response.json()['title'] == title
        blog_id = create_blog_response.json()['id']

        show_blog_response = test_client.get(
            url=f'/blogs/{blog_id}',
            headers={'Authorization': f'Bearer {auth_response.json()["access_token"]}'})

        assert show_blog_response.status_code == 200
        assert show_blog_response.json() == create_blog_response.json()


def test_show_blog_by_id_not_found(test_client: TestClient) -> None:
    username = 'john'
    password = '123'
    blog_id = 0

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

        show_blog_response = test_client.get(
            url=f'/blogs/{blog_id}',
            headers={'Authorization': f'Bearer {auth_response.json()["access_token"]}'})

        assert show_blog_response.status_code == 404
        assert show_blog_response.json() == {'detail': f'Blog with the id {blog_id} is not found'}
