from flask import Flask, render_template, redirect, abort
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from data import db_session
from data.users import User
from data.books import Books
from data.author import Author
from registerform import RegisterForm
from add_authorform import Add_authorForm
from add_book_to_authorform import Add_book_to_authorForm
from loginform import LoginForm
from flask_restful import abort, Api
import books_resources
import authors_resources

app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)

api.add_resource(books_resources.BooksListResource, '/api/books')
api.add_resource(books_resources.BooksResource, '/api/books/<int:books_id>')

api.add_resource(authors_resources.AuthorListResource, '/api/authors')
api.add_resource(authors_resources.AuthorResource, '/api/authors/<int:author_id>')


def main():
    db_session.global_init("db/shop.sqlite")
    app.run()


@app.route('/delete_author_from_db/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_author_from_db(id):
    session = db_session.create_session()
    book = session.query(Books).filter(Books.author_id == id)
    for elem in book:
        if elem:
            session.delete(elem)
            session.commit()
        else:
            abort(404)
    author = session.query(Author).filter(Author.id == id).first()
    if author:
        session.delete(author)
        session.commit()
    else:
        abort(404)
    author = session.query(Author)
    return render_template("list_of_authors.html", author=author)


@app.route('/delete_book_from_db/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_book_from_db(id):
    session = db_session.create_session()
    book = session.query(Books).filter(Books.id == id).first()
    if book:
        session.delete(book)
        session.commit()
    else:
        abort(404)
    books = session.query(Books).filter(Books.author_id == book.author_id)
    author = session.query(Author).filter(Author.id == book.author_id).first()
    author = author.name
    return render_template("books.html", books=books, author=author)


@app.route('/add_book_to_author', methods=['GET', 'POST'])
@login_required
def add_book_to_author():
    form = Add_book_to_authorForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        author = session.query(Author).filter(Author.name == form.name.data).first()
        if session.query(Books).filter(Books.title == form.title.data).first():
            return render_template('add_book_to_author.html', title='Добавление книги автору',
                                   form=form,
                                   message="У этого автора уже есть данная книга")
        books = Books(
            title=form.title.data,
            description=form.description.data,
            price=form.price.data,
            count=100,
            author_id=author.id
        )
        session.add(books)
        session.commit()
        return redirect('/')
    return render_template('add_book_to_author.html', title='Добавление книги автору', form=form)


@app.route('/add_author', methods=['GET', 'POST'])
@login_required
def add_author():
    form = Add_authorForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        if session.query(Author).filter(Author.name == form.name.data).first():
            return render_template('add_author.html', title='Добавление автора',
                                   form=form,
                                   message="Такой автор уже есть")
        author = Author(
            name=form.name.data
        )
        session.add(author)
        session.commit()
        return redirect('/')
    return render_template('add_author.html', title='Добавление автора', form=form)


@app.route('/buy')
def buy():
    session = db_session.create_session()
    user = session.query(User).filter(User.id == current_user.id).first()
    user.shopping_cart = '0'
    session.commit()
    return render_template('base.html',
                           text='Ваш заказ отправлен в обработку. Мы сообщим вам о состоянии заказа по СМС. '
                                'Спасибо, что выбрали наш магазин!')


@app.route('/delete_books/<int:id>')
def delete_books(id):
    session = db_session.create_session()
    book = session.query(Books).filter(Books.id == id).first()
    book.count += 1
    user = session.query(User).filter(User.id == current_user.id).first()
    list_of_books = user.shopping_cart
    user.shopping_cart = ''
    list_of_books = list_of_books.split(',')
    list_of_books = [int(el) for el in list_of_books]
    del list_of_books[list_of_books.index(id)]
    if list_of_books != []:
        user.shopping_cart += str(list_of_books[0])
        for elem in list_of_books[1:]:
            user.shopping_cart += ',' + str(elem)
    else:
        user.shopping_cart = 0
        list_of_books = [0]
    session.commit()
    count = 0
    if user.shopping_cart != '0':
        for id in list_of_books:
            books = session.query(Books).filter(Books.id == id).first()
            count += books.price
    books = session.query(Books)
    return render_template('shopping_cart.html', list_of_books=list_of_books, books=books, count=count)


@app.route('/books/<int:id>')
def show_books(id):
    session = db_session.create_session()
    books = session.query(Books).filter(Books.author_id == id)
    author = session.query(Author).filter(Author.id == id).first()
    author = author.name
    return render_template("books.html", author=author, books=books)


@app.route('/list_of_authors')
def list_of_authors():
    session = db_session.create_session()
    author = session.query(Author)
    return render_template("list_of_authors.html", author=author)


@app.route('/add_books/<int:id>')
def add_books(id):
    session = db_session.create_session()
    books = session.query(Books).filter(Books.id == id).first()
    author_id = books.author_id
    books.count -= 1
    users = session.query(User).filter(User.id == current_user.id).first()
    if users.shopping_cart != '0':
        users.shopping_cart += ',' + str(id)
    else:
        users.shopping_cart = ''
        users.shopping_cart += str(id)
    session.commit()
    books = session.query(Books).filter(Books.author_id == author_id)
    author = session.query(Author).filter(Author.id == author_id).first()
    author = author.name
    return render_template("books.html", books=books, author=author)


@app.route('/shopping_cart')
def shopping_cart():
    session = db_session.create_session()
    user = session.query(User).filter(User.id == current_user.id).first()
    list_of_books = user.shopping_cart
    list_of_books = list_of_books.split(',')
    list_of_books = [int(el) for el in list_of_books]
    count = 0
    if user.shopping_cart != '0':
        for id in list_of_books:
            books = session.query(Books).filter(Books.id == id).first()
            count += books.price
    books = session.query(Books)
    return render_template('shopping_cart.html', list_of_books=list_of_books, books=books, count=count)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(User).filter(User.phone == form.phone.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


@app.route("/")
def main_page():
    return render_template("base.html", text='Добро пожаловать!')


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        session = db_session.create_session()
        if session.query(User).filter(User.phone == form.phone.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            phone=form.phone.data,
            shopping_cart='0'
        )
        user.set_password(form.password.data)
        session.add(user)
        session.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


if __name__ == '__main__':
    main()
