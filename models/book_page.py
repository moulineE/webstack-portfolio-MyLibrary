#!/usr/bin/python3
"""BookPage model"""
import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey, Integer, Text


class Book_page(BaseModel, Base):
    """Book_Page class"""
    __tablename__ = 'book_pages'
    book_id = Column(String(60), ForeignKey('books.id'), nullable=False)
    page_no = Column(Integer, nullable=False)
    content = Column(Text, nullable=False)

    def __init__(self, *args, **kwargs) -> None:
        """initializes book page"""
        super().__init__(*args, **kwargs)
