from flask import Flask, render_template, jsonify, request, session
from sqlalchemy import or_
from models import *


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://dgpohzutvnfioc:b66825f5296b8648d10b630f565dd0bc9d31b99ec0250686b743b59460d80157@ec2-54-217-224-85.eu-west-1.compute.amazonaws.com:5432/d7kd8qe1q0i3h1" #os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/logout", methods=["POST"])
def logout():
	if session['user'] is not None:
		session['user'] = None
		return render_template("index.html")
	else:
		return render_template("error.html", message="No user is currently logged in")


@app.route("/menu", methods=["POST"])
def menu():

	username = request.form.get("name")
	password = request.form.get("password")

	option = request.form.get("option")
	if option=="login":
		check = User.query.filter_by(name=username, password=password).first()
		if check:
			session['user'] = username
			return render_template("search.html")
		return render_template("error.html", message="Username or password is incorrect")

	elif option=="register":
		exists = User.query.filter_by(name=username).first()
		if exists:
			return render_template("error.html", message="Username already exists")
		User.add_user(name=username, passwrd=password)
		return render_template("index.html")


@app.route("/results", methods=["POST"])
def results():
	search = request.form.get("search")
	if isinstance(search, int):
		books = Book.query.filter(Book.publication_year.like(f'{search}%'))
	else:
		books = Book.query.filter(or_(Book.title.like(f'%{search}%'), Book.author.like(f'%{search}%'), Book.isbn.like(f'%{search}%')))
	if books is None:
		return render_template("error.html", message="No books found")
		
	return render_template("results.html", books=books)


@app.route("/results/<int:book_id>")
def book(book_id):
	'''
	book = Book.query.get(book_id)
	if book is None:
		return render_template("error.html", message="There's no such a book")
	reviews = Book.reviews
	'''
	return render_template("book.html", book=book)

@app.route("/success", methods=["POST"])
def reviews():
	rating = request.form.get("rating")
	review = request.form.get("comment")
	isbn = request.form.get("isbn")
	print(isbn)
	user = session['user']
	#book_id = request.form.get("id")
	book  = Book.query.filter_by(isbn=isbn).first()
	if not book:
		return render_template("error.html", message=f"Couldn't find a book")
	book.addReview(username=user, rating=rating, text=review)
	return	render_template("success.html", book=book)