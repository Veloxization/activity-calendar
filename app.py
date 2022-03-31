from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from os import getenv

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "/database/database.db"
db = SQLAlchemy(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route("/login/post", methods=["POST"])
def loginPost():
    return redirect("/")

@app.route("/signup/post", methods=["POST"])
def signupPost():
    return redirect("/")
