#!/usr/bin/python3
"""Book model"""
import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey, Date, Text, Integer, Table
from sqlalchemy.orm import relationship


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

    def __init__(self, *args, **kwargs) -> None:
        """initializes book"""
        super().__init__(*args, **kwargs)
