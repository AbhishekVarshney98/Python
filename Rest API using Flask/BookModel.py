from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import json
from settings import app

db = SQLAlchemy(app)

class Book(db.Model):
    __tablename__='books'
    id=db.Column()
    name=db.Column()
    price=db.Column()
    isbn=db.Column()

