import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Book(db.Model):
    __tablename__ = "books"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    publication_year = db.Column(db.Integer, nullable=False)
    isbn = db.Column(db.String, nullable=False)
    reviews = db.relationship("Review", backref="book", lazy=True)

    def addReview(self, username, rating, text):
        r = review(username=username, rating=rating, text=text, book_id=self.id)
        db.session.add(r)
        db.session.commit()


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)

    def add_user(name, passwrd):
    	u = User(name=name, password=passwrd)
    	db.session.add(u)
    	db.session.commit()


class Review(db.Model):
    __tablename__ = "reviews"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    text = db.Column(db.String, nullable=True)
    book_id = db.Column(db.Integer, db.ForeignKey("books.id"), nullable=False)