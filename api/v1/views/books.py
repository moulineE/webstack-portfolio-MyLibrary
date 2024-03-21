#!/usr/bin/python3
""" Index """
from api.v1.views import app_views
from flask import jsonify, request, Response
from models import storage


@app_views.route('/books', strict_slashes=False)
def get_books() -> Response:
    """ retrieves a list of all books """
    all_books = storage.all_by_cls("Book")
    list_books = []
    for book in all_books.values():
        list_books.append(book.to_dict())
    return jsonify(list_books)


@app_views.route('/search', strict_slashes=False)
def search() -> Response | tuple[Response, int]:
    """
    Search for a book by title
    :return:
    """
    q = request.args.get("q")
    if q is None:
        return jsonify({"error": "no query"}), 400
    results = storage.book_search(q)
    list_books = []
    for book in results:
        list_books.append(book.to_dict())
    return jsonify(list_books)


@app_views.route('/books/<book_id>', strict_slashes=False)
def get_book(book_id) -> Response | tuple[Response, int]:
    """ retrieves a book by id """
    book = storage.pub_get("Book", book_id)
    if book is None:
        return jsonify({"error": "Not found"}), 404
    return jsonify(book.to_dict())


@app_views.route('/books/<book_id>/<page>', strict_slashes=False)
def get_book_page(book_id, page) -> Response | tuple[Response, int]:
    """ retrieves a book page by id and page """
    chapter = storage.get_chapter(book_id, page)
    if chapter is None:
        return jsonify({"error": "Not found"}), 404
    return jsonify({"content": chapter})


@app_views.route('/bookmarks', methods=['GET', 'POST'])
def add_bookmark() -> Response | tuple[Response, int]:
    """
    Add a bookmark to a book or get all bookmarks of a book
    by user id and book id
    :return:
    """
    if request.method == 'GET':
        user_id = request.args.get('user_id')
        book_id = request.args.get('book_id')
        bookmarks = storage.get_bookmarks(user_id, book_id)
        return jsonify([bookmark.to_dict() for bookmark in bookmarks])
    else:
        user_id = request.form['user_id']
        book_id = request.form['book_id']
        page = request.form['page']
        bookmark_name = request.form['bookmark_name']
        storage.add_bookmark(user_id, book_id, page, bookmark_name)
        return jsonify({'success': True}), 200


@app_views.route('/bookmarks/<string:bookmark_id>', methods=['DELETE'])
def delete_bookmark(bookmark_id) -> tuple[Response, int]:
    """
    Delete a bookmark by id
    :param bookmark_id:
    :return:
    """
    bookmark = storage.pub_get("Bookmark", bookmark_id)
    if bookmark is None:
        return jsonify({"error": "Not found"}), 404
    storage.delete(bookmark)
    storage.save()
    return jsonify({'success': True}), 200
