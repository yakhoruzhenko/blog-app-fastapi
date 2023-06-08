import os
from typing import Iterator

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

env = os.getenv('env', 'prod')
DATABASE_URL = 'sqlite:///./blog.db'
TEST_DATABASE_URL = 'sqlite:///./blog_test.db'
engine = create_engine(DATABASE_URL if env == 'prod' else TEST_DATABASE_URL,
                       connect_args={"check_same_thread": False})


SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()


def get_db() -> Iterator[Session]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
