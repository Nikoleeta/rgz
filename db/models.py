from . import db
from flask_login import UserMixin



class users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable=False, unique=True)
    password = db.Column(db.String(102), nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False)

    def repr(self):
        return f"id:{self.id}, username:{self.username}, is_admin:{self.is_admin}"


class books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book = db.Column(db.String(100), nullable=False)
    image_url = db.Column(db.String(1000), nullable=True)
    author = db.Column(db.String(100), nullable=False)
    pages = db.Column(db.Integer, nullable=False)
    publisher = db.Column(db.String(200), nullable=False)
    
    def repr(self):
        return f"id:{self.id}, book:{self.book}, image_url:{self.image_url}, author:{self.author}, pages:{self.pages}, publisher:{self.publisher}"