#!/usr/bin/python3
"""Book model"""
import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey, Date, Text, Integer, Table
from sqlalchemy.orm import relationship

book_languages = Table('book_languages', Base.metadata,
                       Column('book_id', String(60),
                              ForeignKey('books.id')),
                       Column('language_id', String(60),
                              ForeignKey('languages.id')),
                       Column('book_title', String(128)),
                       Column('published_date', Date),
                       Column('book_summary', Text),
                       Column('chapter_count', Integer))


class Book(BaseModel, Base):
    """Book class"""
    __tablename__ = 'books'
    book_title = Column(String(128), nullable=False)
    published_date = Column(Date, nullable=False)
    book_summary = Column(Text, nullable=False)
    author_id = Column(String(60), ForeignKey('authors.id'), nullable=False)
    chapter_count = Column(Integer, nullable=False)
    bookmarks = relationship("Bookmark", backref="books",
                             cascade="all,delete")
    opened_books = relationship("Opened_book", backref="books",
                                cascade="all, delete")
    book_pages = relationship("Book_page", backref="books",
                              cascade="all, delete")
    languages = relationship("Language", secondary=book_languages,
                             backref="books")

    def __init__(self, *args, **kwargs) -> None:
        """initializes book"""
        super().__init__(*args, **kwargs)


class Language(BaseModel, Base):
    """Language class"""
    __tablename__ = 'languages'
    language_name = Column(String(255), nullable=False)

    def __init__(self, *args, **kwargs) -> None:
        """initializes language"""
        super().__init__(*args, **kwargs)
