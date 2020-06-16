from flask import Flask, render_template, jsonify, request
from models import *


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://dgpohzutvnfioc:b66825f5296b8648d10b630f565dd0bc9d31b99ec0250686b743b59460d80157@ec2-54-217-224-85.eu-west-1.compute.amazonaws.com:5432/d7kd8qe1q0i3h1" #os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)


@app.route("/")
def index():
    books = Book.query.all()
    return render_template("index.html", books=books)


@app.route("/menu", methods=["POST"])
def menu():

	username = request.form.get("name")
	password = request.form.get("password")

	option = request.form.get("option")
	if option=="login":
		check = User.query.filter_by(name=username, password=password).first()
		if check:
			return render_template("search.html")
		return render_template("error.html", message="Username or password is incorrect")

	elif option=="register":
		exists = User.query.filter_by(name=username).first()
		if exists:
			print("This username already exists")
			return render_template("error.html", message="Username already exists")
		User.add_user(name=username, passwrd=password)
		return render_template("index.html")


@app.route("/results")
def results(search):
	if isintance(search, int):
		books = db.execute(f"SELECT * FROM books WHERE {search} IN (publication_year);").all()
	else:
		books = db.execute(f"SELECT * FROM books WHERE {search} IN (title, author, isbn);").all()
	return render_template("results.html", books=books)
