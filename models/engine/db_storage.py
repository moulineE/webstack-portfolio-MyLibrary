#!/usr/bin/python3
"""DBStorage engine"""

import models
from models.base_model import BaseModel, Base
from models.user import User
from models.author import Author
from models.book import Book
from models.bookmark import Bookmark
from models.opened_book import Opened_book
from models.book_page import Book_page
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

classes = {"User": User, "Author": Author, "Book": Book,
           "Bookmark": Bookmark, "Opened_book": Opened_book,
           "Book_page": Book_page}
pub_classes = {"Author": Author, "Book": Book, "Book_page": Book_page}


class DBStorage:
    """DBStorage class"""
    __engine = None
    __session = None

    def __init__(self):
        """Initialize DBStorage"""
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format('MyLibrary_dev',
                                             'MyLibrary_dev_pwd',
                                             'localhost',
                                             'MyLibrary_dev_db'))

    def all_by_cls(self, cls):
        """Query on the current database session by class name"""
        new_dict = {}
        for clss in classes:
            if cls is classes[clss] or cls is clss:
                objs = self.__session.query(classes[clss]).all()
                for obj in objs:
                    key = obj.__class__.__name__ + '.' + obj.id
                    new_dict[key] = obj
        return new_dict

    def get_chapter(self, book_id, page_no):
        """get the chapter of the book"""
        book = self.pub_get(Book, book_id)
        if book is None:
            return None
        if int(page_no) < 1 or int(page_no) > book.chapter_count:
            return None
        chapter = self.__session.query(Book_page).filter_by(
            book_id=book_id, page_no=page_no).first()
        return chapter.content

    def new(self, obj):
        """Add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """Commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete from the current database session"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """Create all tables in the database"""
        Base.metadata.create_all(self.__engine)
        sess_factory = sessionmaker(bind=self.__engine,
                                    expire_on_commit=False)
        Session = scoped_session(sess_factory)
        self.__session = Session

    def close(self):
        """Close the session"""
        self.__session.remove()

    def pub_get(self, cls, id):
        """
        Returns the object based on the class name and its ID,
        or None if not found
        :param cls:
        :param id:
        :return obj or None:
        """
        all_cls = models.storage.all_by_cls(cls)
        for value in all_cls.values():
            if value.id == id:
                return value
        return None

    def get_user_by_email(self, email):
        """
        Returns the object based on the class name and its ID,
        or None if not found
        :param cls:
        :param id:
        :return obj or None:
        """
        all_cls = models.storage.all_by_cls(User)
        for value in all_cls.values():
            if value.email == email:
                return value
        return None

    def get_opened_book_by_user_id_and_bookid(self, user_id, book_id):
        """
        Return the opened book object based on the user_id and book_id
        :param book_id:
        :param user_id:
        :return:
        """
        obj = (self.__session.query(Opened_book).
               filter_by(user_id=user_id, book_id=book_id).first())
        return obj

    def add_bookmark(self, user_id, book_id, page, bookmark_name):
        """
        Add a bookmark for a user on a specific page of a book
        :param user_id:
        :param book_id:
        :param page:
        :param bookmark_name:
        :return:
        """
        new_bookmark = Bookmark(user_id=user_id, book_id=book_id,
                                page=page, bookmark_name=bookmark_name)
        self.new(new_bookmark)
        self.save()

    def get_bookmarks(self, user_id, book_id):
        """
        Get bookmarks for a user on a specific book
         :param user_id:
         :param book_id:
         :return: list of Bookmark objects
        """
        return (self.__session.query(Bookmark).
                filter_by(user_id=user_id, book_id=book_id).all())

    def book_search(self, q):
        """search for a book"""
        objs = (self.__session.query(classes['Book']).order_by(Book.book_title)
                .filter(Book.book_title.like('%'+q+'%'))).all()
        return objs

    def count(self, cls):
        """count the number of objects in storage"""
        if cls not in classes.values():
            return None
        else:
            count = len(models.storage.all_by_cls(cls).values())
            return count
