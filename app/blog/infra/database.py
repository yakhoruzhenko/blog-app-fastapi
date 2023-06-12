import os
from sqlite3 import Connection
from typing import Iterator

from sqlalchemy import create_engine, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.pool.base import _ConnectionRecord

env = os.getenv('env', 'prod')
DATABASE_URL = 'sqlite:///./blog.db'
TEST_DATABASE_URL = 'sqlite:///./blog_test.db'
engine = create_engine(DATABASE_URL if env == 'prod' else TEST_DATABASE_URL, pool_size=500,
                       max_overflow=0, connect_args={"check_same_thread": False})


def _fk_pragma_on_connect(dbapi_con: Connection, con_record: _ConnectionRecord) -> None:
    dbapi_con.execute('pragma foreign_keys=ON')


event.listen(engine, 'connect', _fk_pragma_on_connect)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()


def get_db() -> Iterator[Session]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
