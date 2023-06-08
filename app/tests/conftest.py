from typing import Iterable

import pytest
from fastapi.testclient import TestClient

from app.blog.database import Base, engine
from app.main import app


@pytest.fixture(scope='session', autouse=True)
def database() -> Iterable[None]:
    yield
    Base.metadata.drop_all(engine)


@pytest.fixture(scope='session')
def session_test_client() -> TestClient:
    return TestClient(app)
