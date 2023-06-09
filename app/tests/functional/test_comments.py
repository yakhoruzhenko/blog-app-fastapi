from fastapi.testclient import TestClient


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
