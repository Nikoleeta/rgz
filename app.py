from werkzeug.security import check_password_hash, generate_password_hash
from flask import Flask, Blueprint, render_template, request, make_response, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from db import db
from db.models import users, books
from flask_login import UserMixin
from flask_login import login_user, login_required, current_user, logout_user



app = Flask(__name__)


app.secret_key = '12345'
user_db = "nickoleta"
host_ip = "localhost"
host_port = "5432"
database_name = "books"
password = "123"
login_manager = LoginManager(app)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://Julia:123@localhost/Recipes_rgz?client_encoding=utf8'

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{user_db}:{password}@{host_ip}:{host_port}/{database_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
db.init_app(app)

@login_manager.user_loader
def load_users(user_id):
    return users.query.get(int(user_id))

@app.route('/')
@app.route('/index')
def start():
    return redirect('/main', code=302)


@app.route('/main')
def mainpage():
    all_books = books.query.all()
    if current_user.is_authenticated:
        username = current_user.username
    else:
        username = "Кто Вы?"
    return render_template('mainpage.html', username=username,all_books=all_books)


@app.route('/login', methods=['POST', 'GET'])
def loggin():
    error=''
    if request.method=='GET':
        return render_template('login.html')
        
    username_form=request.form.get('username')
    password_form=request.form.get('password')

    my_user=users.query.filter_by(username=username_form).first()
    
    if my_user=='' or password_form=='':
        error='не заполнены поля'
        return render_template('login.html', error=error)
    
    if my_user is not None:
        if check_password_hash(my_user.password, password_form):
            login_user(my_user, remember=False)
            return redirect('/books')
        else:
            error='неверный пароль'
            return render_template('login.html', error=error) 
    else:
        error='такого пользователя не существует'
        return render_template('login.html', error=error) 

    
@app.route('/register', methods=['post', 'get'])
def registerr():
    if request.method == 'GET':
        return render_template("register.html")

    username_form = request.form.get("username")
    password_form = request.form.get("password")

    if not username_form or not password_form:
        return render_template("register.html", errors='Заполните все поля')

    if users.query.filter_by(username=username_form).first():
        return render_template("register.html", errors='Пользователь с таким логином уже существует')

    hashed_password = generate_password_hash(password_form, method="pbkdf2")
    new_user = users(username=username_form, password=hashed_password, is_admin=False)

    db.session.add(new_user)
    db.session.commit()
    return redirect("/login")

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/login')


@app.route('/books', methods=['POST', 'GET'])
def book():
    username = (users.query.filter_by(id=current_user.id).first()).username
    if request.method == 'GET':
        all_books = books.query.all()
        return render_template('mainpage.html', username=username, all_books=all_books)
    else:
        name = request.form.get('name')
        all_books = books.query.filter(books.name.ilike(f'%{name}%'))
        return render_template('mainpage.html', username=username, all_books=all_books)


@app.route('/filter-books', methods=['GET'])
def filter_books():
    book = request.args.get('book')
    author = request.args.get('author')
    pages = request.args.get('pages')
    publisher = request.args.get('publisher')
    
    filtered_books = filter_books_by_params(book, author, pages, publisher)
    
    return render_template('mainpage.html', all_books=filtered_books)

def filter_books_by_params(books, params):
    filtered_books = []

    for book in books:
        is_match = True
        for param, value in params.items():
            if getattr(book, param) != value:
                is_match = False
                break
        if is_match:
            filtered_books.append(book)

    return filtered_books


