from flask_sqlalchemy import SQLAlchemy 
from flask import Flask

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://localhost:5432/events'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 

db = SQLAlchemy(app)


class Person(db.Model):
    __tablename__ = 'persons'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(), nullable=False)

class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    event = db.Column(db.String(), nullable=False)
    date = db.Column(db.String(), nullable=False)
    location = db.Column(db.String(), nullable=False)
    website = db.Column(db.String(), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey(Person.id), foreign_key=True)

