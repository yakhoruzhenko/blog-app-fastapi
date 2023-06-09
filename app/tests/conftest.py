import random
import string
from typing import Iterable

import pytest
from fastapi.testclient import TestClient

from app.blog.database import Base, engine
from app.main import app


@pytest.fixture(scope='function', autouse=True)
def database() -> Iterable[None]:
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)


@pytest.fixture(scope='session')
def test_client() -> TestClient:
    return TestClient(app)


def random_string(k: int = 10) -> str:
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=k))
