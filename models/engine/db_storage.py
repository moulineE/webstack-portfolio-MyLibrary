#!/usr/bin/python3
"""DBStorage engine"""

import models
from models.base_model import BaseModel, Base
from models.user import User
from models.author import Author
from models.book import Book, Language, Book_by_languages
from models.bookmark import Bookmark
from models.opened_book import Opened_book
from models.book_page import Book_page
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, joinedload
from typing import Dict, Type

classes = {"User": User, "Author": Author, "Book": Book,
           "Bookmark": Bookmark, "Opened_book": Opened_book,
           "Book_page": Book_page, "Language": Language,
           "Book_by_languages": Book_by_languages}
pub_classes = {"Author": Author, "Book": Book, "Book_page": Book_page}


class DBStorage:
    """DBStorage class"""
    __engine = None
    __session = None

    def __init__(self) -> None:
        """Initialize DBStorage"""
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format('MyLibrary_dev',
                                             'MyLibrary_dev_pwd',
                                             'localhost',
                                             'MyLibrary_webstack_dev_db'))

    def all_by_cls(self, cls: Type[BaseModel] | str) -> Dict:
        """Query on the current database session by class name"""
        new_dict = {}
        for clss in classes:
            if cls is classes[clss] or cls is clss:
                objs = self.__session.query(classes[clss]).all()
                for obj in objs:
                    key = obj.__class__.__name__ + '.' + obj.id
                    new_dict[key] = obj
        return new_dict

    def get_chapter(self, book_id: str, page_no: int, lang: str) -> str | None:
        """get the chapter of the book"""
        book = self.get_book_by_lang(book_id, lang)
        if book is None:
            return None
        if int(page_no) < 1 or int(page_no) > book.chapter_count:
            return None
        lang_id = self.__session.query(Language).filter_by(
            language_name=lang).first().id
        chapter = self.__session.query(Book_page).filter_by(
            book_id=book_id, page_no=page_no, language_id=lang_id).first()
        return chapter.content

    def new(self, obj: BaseModel) -> None:
        """Add the object to the current database session"""
        self.__session.add(obj)

    def save(self) -> None:
        """Commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj: BaseModel = None) -> None:
        """Delete from the current database session"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self) -> None:
        """Create all tables in the database"""
        Base.metadata.create_all(self.__engine)
        sess_factory = sessionmaker(bind=self.__engine,
                                    expire_on_commit=False)
        Session = scoped_session(sess_factory)
        self.__session = Session

    def close(self) -> None:
        """Close the session"""
        self.__session.remove()

    def get_session(self):
        """Returns the current SQLAlchemy Session"""
        return self.__session

    def pub_get(self, cls: Type[BaseModel], id: str) -> BaseModel | None:
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

    def get_user_by_email(self, email: str) -> User | None:
        """
        Returns the object based on the class name and its ID,
        or None if not found
        :param email:
        :return obj or None:
        """
        all_cls = models.storage.all_by_cls(User)
        for value in all_cls.values():
            if value.email == email:
                return value
        return None

    def get_opened_book_by_user_id_and_bookid(
            self, user_id: str, book_id: str) -> Opened_book | None:
        """
        Return the opened book object based on the user_id and book_id
        :param book_id:
        :param user_id:
        :return:
        """
        obj = (self.__session.query(Opened_book).
               filter_by(user_id=user_id, book_id=book_id).first())
        return obj

    def add_bookmark(self,
                     user_id: str,
                     book_id: str,
                     page: int,
                     bookmark_name: str) -> None:
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

    def get_bookmarks(self, user_id: str,
                      book_id: str) -> list[Type[Bookmark]] | None:
        """
        Get bookmarks for a user on a specific book
         :param user_id:
         :param book_id:
         :return: list of Bookmark objects
        """
        return (self.__session.query(Bookmark).
                filter_by(user_id=user_id, book_id=book_id).all())

    def book_search(self, q: str) -> list[Type[Book]]:
        """search for a book"""
        objs = (self.__session.query(classes['Book_by_languages']).
                order_by(Book_by_languages.book_title)
                .filter(Book_by_languages.book_title.like('%'+q+'%'))).all()
        return objs

    def count(self, cls: Type[BaseModel] | str) -> int | None:
        """count the number of objects in storage"""
        if cls not in classes.values():
            return None
        else:
            count = len(models.storage.all_by_cls(cls).values())
            return count

    def get_book_languages(self, book_id):
        """get a list of languages of a book"""
        book = self.__session.query(Book).options(
            joinedload(Book.languages)).get(book_id)
        if book is None:
            print(f"No book found with id {book_id}")
            return None
        languages_ids = [language.id for language in book.languages]
        return languages_ids

    def get_lang_by_lang_id(self, lang_id):
        """get a language by its id"""
        lang = self.__session.query(Language).get(lang_id)
        if lang is None:
            print(f"No language found with id {lang_id}")
            return None
        return lang.language_name

    def get_book_by_lang(self, book_id, lang):
        """get a book by its language"""
        lang_id = self.__session.query(Language).filter_by(
            language_name=lang).first().id
        book = self.__session.query(Book).options(
            joinedload(Book.by_languages)).get(book_id)
        if book is None:
            print(f"No book found with id {book_id}")
            return None
        for book_lang in book.by_languages:
            if book_lang.language_id == lang_id:
                return book_lang
        return None

    def get_lang_id_by_lang_name(self, lang: str) -> str:
        """get a language by its id"""
        lang = self.__session.query(Language).filter_by(
            language_name=lang).first()
        if lang is None:
            print(f"No language found with id {lang}")
            return None
        return lang.id
