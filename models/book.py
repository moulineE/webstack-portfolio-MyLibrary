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
                       Column('book_languages_lang_id', String(60),)
                       )


class Book(BaseModel, Base):
    """Book class"""
    __tablename__ = 'books'
    author_id = Column(String(60), ForeignKey('authors.id'), nullable=False)
    bookmarks = relationship("Bookmark", backref="books",
                             cascade="all,delete")
    opened_books = relationship("Opened_book", backref="books",
                                cascade="all, delete")
    book_pages = relationship("Book_page", backref="books",
                              cascade="all, delete")
    by_languages = relationship("Book_by_languages", backref="books")
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


class Book_by_languages(BaseModel, Base):
    """Book_by_languages class"""
    __tablename__ = 'book_by_languages'
    book_id = Column(String(60), ForeignKey('books.id'), primary_key=True)
    language_id = Column(String(60), ForeignKey('languages.id'),
                         primary_key=True)
    book_title = Column(String(128), nullable=False)
    published_date = Column(Date, nullable=False)
    book_summary = Column(Text, nullable=False)
    chapter_count = Column(Integer, nullable=False)

    language = relationship("Language", backref="book_by_languages")

    def __init__(self, *args, **kwargs) -> None:
        """initializes Book_by_languages"""
        super().__init__(*args, **kwargs)
        self.add_to_book_languages()

    def add_to_book_languages(self):
        """Adds a new row to the book_languages table"""
        new_book_language = book_languages.insert().values(
            book_id=self.book_id,
            language_id=self.language_id,
        )
        models.storage.get_session().execute(new_book_language)
        models.storage.save()
