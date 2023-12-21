from werkzeug.security import check_password_hash, generate_password_hash
from flask import Flask, Blueprint, render_template, request, make_response, redirect,  url_for, abort
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from db import db
from db.models import users, books
from flask_login import UserMixin
from flask_login import login_user, login_required, current_user, logout_user
import re


app = Flask(__name__)


app.secret_key = '12345'
user_db = "nickoleta"
host_ip = "nickoleta.mysql.pythonanywhere-services.com"
host_port = "3306"
database_name = "nickoleta$books"
password = "postgres"

# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://Julia:123@localhost/Recipes_rgz?client_encoding=utf8'

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://{user_db}:{password}@{host_ip}:{host_port}/{database_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)

@login_manager.user_loader
def load_users(user_id):
    return users.query.get(int(user_id))


@app.route('/')
@app.route('/index')
def start():
    return redirect('/main', code=302)


# @app.route('/main', methods=['POST', 'GET'])
# def mainpage():
#     if current_user.is_authenticated:
#         username = current_user.username
#     else:
#         username = "Кто Вы?"
#     offset = request.args.get('offset', default=0, type=int)
#     books_list = books.query.limit(20).offset(offset).all()
#     return render_template('mainpage.html', all_books=books_list, username=username)


@app.route('/main', methods=['POST', 'GET'])
def mainpage():
    if current_user.is_authenticated:
        username = current_user.username
    else:
        username = "Кто Вы?"
    
    if request.method == 'POST':
        book_title = request.form.get('book')
        author = request.form.get('author')
        min_pages = request.form.get('min_pages')
        max_pages = request.form.get('max_pages')
        publisher = request.form.get('publisher')
        
        # Выполнить фильтрацию на основе введенных пользователем параметров
        filtered_books_list = filter_books_logic(book_title, author, min_pages, max_pages, publisher)
        return render_template('mainpage.html', all_books=filtered_books_list, username=username)

    else:
        # Раздел для отображения всех книг без фильтрации
        offset = request.args.get('offset', default=0, type=int)
        books_list = books.query.limit(20).offset(offset).all()
        return render_template('mainpage.html', all_books=books_list, username=username)

def filter_books_logic(book_title, author, min_pages, max_pages, publisher):
    query = books.query
    if book_title:
        query = query.filter(books.book.ilike(f"%{book_title}%"))
    if author:
        query = query.filter(books.author.ilike(f"%{author}%"))
    if min_pages:
        query = query.filter(books.pages >= int(min_pages))
    if max_pages:
        query = query.filter(books.pages <= int(max_pages))
    if publisher:
        query = query.filter(books.publisher.ilike(f"%{publisher}%"))

    return query.all()



@app.route('/login', methods=['POST', 'GET'])
def login():
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
            return redirect('/main')
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
    
    if not re.match("^[a-zA-Z0-9!@#$%^&*]+$", username_form) or not re.match("^[a-zA-Z0-9!@#$%^&*]+$", password_form):
        return render_template("register.html", errors='Логин и пароль должны состоять только из латинских букв, цифр и знаков препинания')
    
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


@app.route('/deleteacc')
@login_required
def deleteacc():
    admin = users.query.filter_by(id=current_user.id).first().is_admin
    if admin:
        return redirect("/main")
    delUser = users.query.filter_by(id=current_user.id).first()
    logout_user()
    db.session.delete(delUser)
    db.session.commit()
    return redirect("/main")


@app.route('/books', methods=['POST', 'GET'])
@login_required
def book():
    if current_user.is_authenticated:
        username = current_user.username
        if request.method == 'GET':
            all_books = books.query.all()
            return render_template('mainpage.html', username=username, all_books=all_books)
        elif request.method == 'POST':
            name = request.form.get('name')
            author = request.form.get('author')
            pages = request.form.get('pages')
            publisher = request.form.get('publisher')

            filtered_books = books.query.filter(
                books.name.ilike(f'%{name}%'),
                books.author.ilike(f'%{author}%'),
                books.publisher.ilike(f'%{publisher}%')
            ).all()

            return render_template('mainpage.html', username=username, all_books=filtered_books)
    else:
        abort(404)


@app.route('/addbook', methods=['POST', 'GET'])
def add():
    admin = users.query.filter_by(id=current_user.id).first().is_admin
    if admin:
        username = (users.query.filter_by(id=current_user.id).first()).username
        if request.method == 'GET':
            return render_template("add.html", username=username)
        else:
            book = request.form.get("book")
            author = request.form.get("author")
            pages = request.form.get("pages")
            publisher = request.form.get("publisher")
            photo = request.form.get("photo")

            if not book or not author or not pages or not publisher or not photo:
                errors = "Заполните все поля"
                return render_template('add.html', username=username, errors=errors)
            id=books.query.order_by(books.id.desc()).first().id+1
            newbook = books(
                id=id,
                book=book,
                author=author,
                image_url=photo, 
                pages=pages,
                publisher=publisher
            )
            db.session.add(newbook)
            db.session.commit()

            return redirect('/main', code=302)
    else:
        return redirect('/main')


@app.route('/delete', methods=['POST', 'GET'])
def delete():
    admin = users.query.filter_by(id=current_user.id).first().is_admin
    if admin:
        username = (users.query.filter_by(id=current_user.id).first()).username
        all_books=books.query.all()
        idbook=request.form.get("delete_book")
        if request.method == 'GET':
            return render_template("delete.html", username=username, all_books=all_books)
        else:
            delete_book=books.query.filter_by(id=idbook).first()
            db.session.delete(delete_book)
            db.session.commit()

            return redirect('/main', code=302)
    else:
        return redirect('/main')
    

@app.route('/edit/', methods=['POST', 'GET'])
def edit():
    admin = users.query.filter_by(id=current_user.id).first().is_admin
    if admin:
        username = (users.query.filter_by(id=current_user.id).first()).username
        all_books=books.query.all()
        idbook=request.form.get("delete_book")
        if request.method == 'GET':
            return render_template("edit_choose.html", username=username, idbook=idbook, all_books=all_books)
        else:
            idbook=request.form.get("delete_book")
            return redirect(f'/edit/{idbook}', code=302)
    else:
        return redirect('/main')


@app.route('/edit/<int:idbook>', methods=['POST', 'GET'])
def editbook(idbook):
    admin = users.query.filter_by(id=current_user.id).first().is_admin
    if admin:
        username = (users.query.filter_by(id=current_user.id).first()).username
        booktoedit = books.query.get(idbook)
        if request.method == 'GET':
            return render_template("edit.html", username=username, book=booktoedit)
        else:
            book = request.form.get("book")
            author = request.form.get("author")
            pages = request.form.get("pages")
            publisher = request.form.get("publisher")
            photo = request.form.get("photo")

            if not book or not author or not pages or not publisher or not photo:
                errors = "Заполните все поля"
                return render_template('edit.html', username=username, errors=errors, book=booktoedit)

            booktoedit.book = book
            booktoedit.author = author
            booktoedit.pages = pages
            booktoedit.publisher = publisher
            booktoedit.imageurl = photo

            db.session.commit()

            return redirect('/main', code=302)
    else:
        return redirect('/main')


@app.route('/book20',  methods=['POST', 'GET'])
def next_books():
    if current_user.is_authenticated:
        username = current_user.username
        offset = request.args.get('offset', default=20, type=int)
        if offset <100:
            books_per_page = 20 
            all_books = books.query.all() 
            current_books = all_books[offset:offset + books_per_page]  
            return render_template('mainpage.html', all_books=current_books, offset=offset + books_per_page, username=username)
        else:
            return redirect('/main')
    else:
            return redirect('/login')
    


@app.route('/previous_books', methods=['POST', 'GET'])
def previous_books():
    if current_user.is_authenticated:
        username = current_user.username
        offset = request.args.get('offset', default=20, type=int)
        books_per_page = 20 
        all_books = books.query.all() 
        if offset - books_per_page > 0:
            previous_books = all_books[offset - books_per_page:offset]
            return render_template('mainpage.html', all_books=previous_books, offset=offset - books_per_page,  username=username)
        else:
            return redirect('/main' )
    else:
            return redirect('/login' )

