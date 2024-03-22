#!/usr/bin/python3
"""OpenedBook model"""
import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey, Integer, Boolean


class Opened_book(BaseModel, Base):
    """Opened_book class"""
    __tablename__ = 'opened_books'
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    book_id = Column(String(60), ForeignKey('books.id'), nullable=False)
    page = Column(Integer, nullable=False)
    read = Column(Boolean, default=False, nullable=False)

    def __init__(self, *args, **kwargs) -> None:
        """initializes opened book"""
        super().__init__(*args, **kwargs)
