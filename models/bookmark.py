#!/usr/bin/python3
"""Bookmark model"""
import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey, Integer


class Bookmark(BaseModel, Base):
    """Bookmark class"""
    __tablename__ = 'bookmarks'
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    book_id = Column(String(60), ForeignKey('books.id'), nullable=False)
    page = Column(Integer, nullable=False)
    bookmark_name = Column(String(128), nullable=False)

    def __init__(self, *args, **kwargs) -> None:
        """initializes bookmark"""
        super().__init__(*args, **kwargs)
