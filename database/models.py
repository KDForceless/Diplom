from sqlalchemy import (Column, String, Integer, Text,
                        Float, DateTime, ForeignKey, Boolean,
                        Date)
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String, unique=True)
    phone_number = Column(String, unique=True)
    email = Column(String, nullable=False, unique=True)
    user_city = Column(String, nullable=True)
    password = Column(String, nullable=False)
    reg_date = Column(DateTime)
    #book = relationship("Book", back_populates="user_fk")


# class Hashtag(Base):
#     __tablename__ = "hashtags"
#     id = Column(Integer, autoincrement=True, primary_key=True)
#     hashtag_name = Column(String, nullable=False, unique=True)
#     reg_date = Column(DateTime)


# class Book(Base):
#     __tablename__ = 'books'
#     id = Column(Integer, primary_key=True, index=True)
#     user_id = Column(Integer, ForeignKey("users.id"))
#     hashtag = Column(String, ForeignKey("hashtags.hashtag_name"), nullable=True)
#     photo_id = Column(Integer, ForeignKey("book_photos.id"))
#     filename = Column(String, unique=True, index=True)
#     content = Column(String)
#     file_type = Column(String)
#     photo_fk = relationship("BookPhoto", lazy="subquery", back_populates="posts", cascade="all, delete",
#                            passive_deletes=True)
#     user_fk = relationship("User", lazy="subquery", back_populates="posts", cascade="all, delete",
#                            passive_deletes=True)
#     hashtag_fk = relationship("Hashtag", lazy="subquery")


# class BookPhoto(Base):
#     __tablename__ = "book_photos"
#     id = Column(Integer, autoincrement=True, primary_key=True)
#     book_id = Column(Integer, ForeignKey("books.id"))
#     photo_name = Column(String, nullable=False)
#     photo_path = Column(String, nullable=False)
#     reg_date = Column(DateTime)
#     post_fk = relationship(Book, lazy="subquery")


class Comment(Base):
    __tablename__ = "comments"
    id = Column(Integer, autoincrement=True, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    text = Column(String, nullable=False)
    reg_date = Column(DateTime)
    user_fk = relationship(User, lazy="subquery")

