from flask import Flask, render_template, redirect, request, session
from flask_sqlalchemy import SQLAlchemy
from src.actions.actions import Actions
from os import getenv

app = Flask(__name__, static_url_path='')
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URI")
app.secret_key = getenv("SECRET_KEY")
db = SQLAlchemy(app)
actions = Actions(db)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login")
def login():
    error = request.args.get('error')
    return render_template("login.html", error=error)

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")

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
    if actions.check_login(username, password):
        session["username"] = username
        return redirect("/")
    return redirect("/login?error=login-error")

@app.route("/creategroup")
def createGroup():
    if not session["username"]:
        return render_template("404.html"), 404
    if not actions.user_can_create_group(session["username"]):
        return render_template("404.html"), 404
    return render_template("creategroup.html")

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
    session["username"] = username
    if group == "new":
        actions.create_user(username, password, True)
        return redirect(f"/creategroup")
    actions.create_user(username, password, False, int(group))
    return redirect("/")

@app.route("/creategroup/post", methods=["POST"])
def createGroupPost():
    group_name = request.form["group-name"]
    username = session["username"]
    if not actions.user_can_create_group(username):
        return render_template("404.html"), 404
    error = actions.check_group_name(group_name)
    if error:
        return redirect(f"/creategroup?error={error}")
    group_id = actions.create_group(group_name)
    actions.add_user_to_group(username, group_id)
    return redirect("/")

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404
