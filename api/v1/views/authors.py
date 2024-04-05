#!/usr/bin/python3
""" api for authors """
from api.v1.views import app_views
from flask import jsonify, Response
from models import storage


@app_views.route('/authors', strict_slashes=False)
def get_authors() -> Response:
    """ retrieves a list of all authors """
    all_authors = storage.all_by_cls("Author")
    list_authors = []
    for author in all_authors.values():
        list_authors.append(author.to_dict())
    return jsonify(list_authors)


@app_views.route('/authors/<author_id>', strict_slashes=False)
def get_author(author_id) -> Response | tuple[Response, int]:
    """ retrieves an author by id """
    author = storage.pub_get("Author", author_id)
    if author is None:
        return jsonify({"error": "Not found"}), 404
    return jsonify(author.to_dict())


@app_views.route('/authors_by_book/<book_id>', strict_slashes=False)
def get_author_by_book_id(book_id) -> Response | tuple[Response, int]:
    """ retrieves an author by book_id """
    book = storage.pub_get("Book", book_id)
    author = storage.pub_get("Author", book.author_id)
    if author is None:
        return jsonify({"error": "Not found"}), 404
    return jsonify(author.to_dict())


@app_views.route('/authors/<author_id>/books', strict_slashes=False)
def get_author_books(author_id) -> Response | tuple[Response, int]:
    """ retrieves a list of all books of an author """
    all_books = storage.all_by_cls("Book")
    list_books = []
    for book in all_books.values():
        if book.author_id == author_id:
            list_books.append(book.to_dict())
    if list_books == []:
        return jsonify({"error": "Not found"}), 404
    return jsonify(list_books)
