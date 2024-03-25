#!/usr/bin/python3
"""User model"""
import models
from models.base_model import BaseModel, Base
import sqlalchemy
from sqlalchemy import Column, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash


class User(BaseModel, Base):
    """User class"""
    __tablename__ = 'users'
    first_name = Column(String(128), nullable=False)
    last_name = Column(String(128), nullable=False)
    email = Column(String(128), unique=True, nullable=False)
    password = Column(String(256), nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    language_id = Column(String(60), ForeignKey('languages.id'),
                         nullable=False)
    upload_perm = Column(Boolean, default=False, nullable=False)
    bookmarks = relationship("Bookmark", backref="users",
                             cascade="all, delete")
    opened_books = relationship("Opened_book", backref="users",
                                cascade="all, delete")

    @property
    def is_authenticated(self) -> bool:
        return True

    @property
    def is_anonymous(self) -> bool:
        return False

    def get_id(self) -> str:
        return str(self.id)

    def __init__(self, *args, **kwargs) -> None:
        """initializes user"""
        super().__init__(*args, **kwargs)
        self.password = generate_password_hash(kwargs.get('password'))

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password, password)
