#!/usr/bin/python3
""" Flask Application """
from flask import (Flask, render_template, make_response, jsonify,
                   request, redirect, url_for, Response)
from flask_login import (LoginManager, login_user, logout_user,
                         login_required, current_user)
from flask_cors import CORS
from models import storage
from models.user import User
from models.opened_book import Opened_book
from models.base_model import BaseModel
from api.v1.views import app_views
from werkzeug.security import generate_password_hash


login_manager = LoginManager()

app = Flask(__name__)
app.register_blueprint(app_views)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.secret_key = 'S6YDuvuw$f*wRp6a!TvVX&cxSaU$6'
cors = CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
login_manager.init_app(app)


@app.teardown_appcontext
def close_db(error):
    """ Close Storage """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """ 404 Error
    ---
    responses:
      404:
        description: a resource was not found
    """
    return make_response(jsonify({'error': "Not found"}), 404)


@login_manager.user_loader
def load_user(user_id: str) -> User | None:
    """
    retrieve the corresponding User object from the storage system
    to Flask-Login
    :param user_id:
    :return:
    """
    return storage.pub_get(User, user_id)


@app.route('/mylibrary/login', methods=['GET', 'POST'])
def login() -> str | Response:
    """
    Login route for the user to login to the app and
    access the app user features
    :return:
    """
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = storage.get_user_by_email(email)
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('home_page'))
        return make_response(jsonify({'error': "Invalid email,"
                                               " or password"}), 401)
    return render_template('login.html')


@app.route('/mylibrary/logout')
@login_required
def logout() -> Response:
    """
    logout route for the user to logout of the app
    and redirect to the home page
    :return:
    """
    logout_user()
    return redirect(url_for('home_page'))


@app.route('/mylibrary/register', methods=['GET', 'POST'])
def register() -> str | Response:
    """
    Register route for the user to register an account with the app
    :return:
    """
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']
        user = User(first_name=first_name, last_name=last_name,
                    email=email, password=password)
        BaseModel.save(user)
        login_user(user)
        return redirect(url_for('home_page'))
    return render_template('register.html')


@app.route('/mylibrary/profile', methods=['GET', 'POST'])
@login_required
def profile() -> str | Response:
    """
    Profile route for the user to update their profile
    :return:
    """
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        password = request.form.get('password')
        user = current_user
        if first_name:
            user.first_name = first_name
        if last_name:
            user.last_name = last_name
        if email:
            user.email = email
        if password:
            user.password = generate_password_hash(password)
        BaseModel.save(user)
        return redirect(url_for('home_page'))
    return render_template('profile.html', user=current_user)


@app.route('/', strict_slashes=False)
def landing_page() -> str:
    """
    Landing page
    :return:
    """
    return render_template('landing.html')


@app.route('/mylibrary')
@app.route('/mylibrary/index.html')
def home_page() -> str:
    """
    Home page route
    :return:
    """
    if current_user.is_authenticated:
        return render_template('index.html', user=current_user)
    return render_template('index.html')


@app.route('/mylibrary/books', strict_slashes=False)
def all_books() -> str:
    """
    All books route (not used in the app - for future use)
    :return:
    """
    all_books = storage.all_by_cls("Book")
    list_books = []
    for book in all_books.values():
        author = storage.pub_get("Author", book.author_id)
        book = book.to_dict()
        book['author_name'] = ("{} {}"
                               .format(author.first_name, author.last_name))
        list_books.append(book)
    return render_template('index.html', books=list_books)


@app.route('/mylibrary/book', strict_slashes=False)
def book() -> str | Response:
    """
    Book route to view a book and its chapters by page number and book_id
    and updating user opened_book
    :return:
    """
    page = 1
    book_id = request.args.get('id')
    if request.args.get('page'):
        page = request.args.get('page')
    page = int(page)
    if page < 1:
        page = 1
    book = storage.pub_get("Book", book_id)
    if not book:
        return make_response(jsonify({'error': "Book not found,"
                                               " check the book_id"}), 404)
    author = storage.pub_get("Author", book.author_id)
    if not author:
        return make_response(jsonify({'error': "Author not found"}), 404)
    book = book.to_dict()
    book['author_name'] = "{} {}".format(author.first_name, author.last_name)
    if page > book['chapter_count']:
        page = book['chapter_count']
    chapter = storage.get_chapter(book_id, page)
    if current_user.is_authenticated:
        opened_book = storage.get_opened_book_by_user_id_and_bookid(
            current_user.id, book_id)
        if opened_book:
            # Update opened_book as necessary
            if page == 1 and opened_book.page != 1:
                return redirect(url_for('book', id=book_id,
                                        page=opened_book.page, ))
            if page > opened_book.page:
                opened_book.page = page
            if page == book['chapter_count']:
                opened_book.read = True
            BaseModel.save(opened_book)
            pass
        else:
            # Create a new Opened_book
            opened_book = Opened_book(user_id=current_user.id, book_id=book_id,
                                      page=1, read=False)
            BaseModel.save(opened_book)
        return render_template('book.html', user=current_user,
                               book=book, chapter=chapter, page=page)
    return render_template('book.html', book=book, chapter=chapter, page=page)


if __name__ == '__main__':
    app.run(debug=True, threaded=True)
