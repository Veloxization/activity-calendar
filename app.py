from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash
from src.actions.actions import Actions
from os import getenv

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URI")
db = SQLAlchemy(app)
actions = Actions(db)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/signup")
def signup():
    groups = actions.get_groups()
    return render_template("signup.html", groups=groups)

@app.route("/login/post", methods=["POST"])
def loginPost():
    username = request.form["username"]
    password = request.form["password"]
    return redirect("/")

@app.route("/signup/post", methods=["POST"])
def signupPost():
    username = request.form["username"]
    password = request.form["password"]
    password_again = request.form["password-again"]
    if actions.username_taken(username):
        return redirect("/signup?error=username-taken")
    if password != password_again:
        return redirect("/signup?error=no-match")
    return redirect("/")
