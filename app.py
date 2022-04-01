from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash
from src.actions.actions import Actions
from os import getenv

app = Flask(__name__, static_url_path='')
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
    error = request.args.get('error')
    if error:
        error = error.replace("-", " ")
        error = error.capitalize()
    return render_template("signup.html", groups=groups, error=error)

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
    group = request.form["group"]
    form_input = f"username={username}&group={group}"
    username_error = actions.check_username(username)
    if username_error:
        return redirect(f"/signup?error={username_error}&{form_input}")
    password_error = actions.check_password(password, password_again)
    if password_error:
        return redirect(f"/signup?error={password_error}&{form_input}")
    if group == "new":
        return redirect(f"/creategroup?username={username}")
    return redirect("/")

@app.route("/creategroup/post", methods=["POST"])
def createGroupPost():
    group_name = request.form["group-name"]
    error = actions.check_group_name(group_name)
    if error:
        return redirect(f"/creategroup?error={error}")
    return redirect("/")
