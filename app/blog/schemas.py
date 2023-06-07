from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class Blog(Base):
    __tablename__ = 'blogs'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True)
    body = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))
    creator = relationship('User', back_populates='blogs')


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    email = Column(String)
    password = Column(String)
    secret = Column(String, nullable=True)
    blogs = relationship('Blog', back_populates='creator')
