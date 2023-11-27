from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class Blog(Base):
    __tablename__ = 'blogs'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True, nullable=False)
    body = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    creator = relationship('User', back_populates='blogs')
    comments = relationship('Comment')


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    secret = Column(String, nullable=True)
    blogs = relationship('Blog', back_populates='creator')
    comments = relationship('Comment')


class Comment(Base):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, nullable=False)
    user_name = Column(String, ForeignKey('users.name', ondelete='CASCADE'))
    blog_title = Column(String, ForeignKey('blogs.title', ondelete='CASCADE'))
    creator = relationship('User', back_populates='comments')
    blog = relationship('Blog', back_populates='comments')
