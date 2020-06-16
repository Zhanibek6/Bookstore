import csv
import os

from flask import Flask, render_template, request
from models import *

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] =  "postgres://dgpohzutvnfioc:b66825f5296b8648d10b630f565dd0bc9d31b99ec0250686b743b59460d80157@ec2-54-217-224-85.eu-west-1.compute.amazonaws.com:5432/d7kd8qe1q0i3h1"  #os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

def main():
    f = open("books.csv")
    reader = csv.reader(f)
    for isbn, title, author, publication_year in reader:
        book = Book(title=title, author=author, publication_year=publication_year, isbn=isbn)
        db.session.add(book)
        print(f"Added book with title {title}, author {author}, isbn {isbn} which was published in {publication_year}.")
    db.session.commit()

if __name__ == "__main__":
    with app.app_context():
        main()
