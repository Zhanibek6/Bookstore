from flask import Flask, render_template, jsonify, request
from models import *


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://abfqprtnmjmzrt:336db6044bedcf620c4ce47070642e937396b7c5633d24d07b759103d3bbd9ce@ec2-54-247-79-178.eu-west-1.compute.amazonaws.com:5432/d6tia03nnbe25e" #os.getenv("DATABASE_URL")
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
	if option=="login"
		check = Flight.query.filter_by(name=username, password=password).first()
		if check:
			return render_template("search.html")
		return render_template("error.html", message="Username or password is incorrect")

	elif option=="register":
		exists = Flight.query.filter_by(name=username).first()
		if exists:
			print("This username already exists")
			return render_template("error.html", message="Username already exists")
		User.add_user(username, password)
		return render_template("index.html")


@app.route("/results")
def results(search):
	books = Book.query.all() 

