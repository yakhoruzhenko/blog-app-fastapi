from __future__ import annotations

from locust import HttpUser, TaskSet, between, tag, task
from tests.conftest import random_string


class BlogAppTasks(TaskSet):
    wait_time = between(0.1, 0.2)

    @tag('Post blog')
    @task(1)
    def post_blog(self: BlogAppTasks) -> None:
        self.client.post(
            url='blogs', json=dict(title=random_string(), body=random_string()),
            headers={'Authorization': f'Bearer {self.client.token}'})

    @tag('View User\'s profile and update password')
    @task(2)
    def get_user_profile_and_update_password(self: BlogAppTasks) -> None:
        get_profile_response = self.client.get(
            url='users',
            headers={'Authorization': f'Bearer {self.client.token}'})

        data = get_profile_response.json()

        self.client.put(url='users', json=dict(name=data['name'],
                                               password=random_string(),
                                               email=data['email'],
                                               secret=self.client.secret))


class LoadTester(HttpUser):
    """
    Sets loadtest configuration.
    """
    tasks = [BlogAppTasks]

    # Set up stage
    @tag('User setup stage')
    def on_start(self: HttpUser) -> None:
        username = random_string()
        password = random_string()
        secret = random_string()
        self.client.post(url='users', json=dict(name=username,
                                                password=password,
                                                email=random_string(),
                                                secret=secret))
        auth_response = self.client.post(url='login', data=dict(username=username,
                                                                password=password))
        self.client.token = auth_response.json()['access_token']
        self.client.secret = secret
