from flask import Flask, render_template, redirect, request, session, abort
from flask_sqlalchemy import SQLAlchemy
from src.actions.actions import Actions
from os import getenv
import secrets

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
    del session["csrf_token"]
    return redirect("/")

@app.route("/signup")
def signup():
    groups = actions.get_groups()
    error = request.args.get('error')
    if error:
        error = error.replace("-", " ")
        error = error.capitalize()
    return render_template("signup.html", groups=groups, error=error)

@app.route("/group")
def group():
    if not session["username"]:
        abort(403)
    group = actions.get_user_group(session["username"])
    if group is None:
        return redirect("/group/create")
    member_count = len(actions.get_group_members(group.id))
    admins = actions.get_group_admins(group.id)
    members = actions.get_group_regular_members(group.id)
    return render_template("group.html", group=group, member_count=member_count, admins=admins, members=members)

@app.route("/group/create")
def create_group():
    if not session["username"]:
        abort(403)
    if not actions.user_can_create_group(session["username"]):
        abort(403)
    error = request.args.get('error')
    if error:
        error = error.replace("-", " ")
        error = error.capitalize()
    return render_template("creategroup.html", error=error)

@app.route("/activities")
def activities():
    if not session["username"]:
        abort(403)
    user_activity = actions.get_user_activity(session["username"])
    if user_activity:
        active = actions.get_activity(user_activity.activity_id)
    else:
        active = None
    group = actions.get_user_group(session["username"])
    if not group:
        return redirect("/group/create")
    user = actions.find_user(session["username"])
    activities = actions.get_group_activities(group.id)
    return render_template("activities.html", active=active, user_activity=user_activity, activity_count=len(activities), user=user, activities=activities)

@app.route("/activities/create")
def create_activity():
    if not session["username"]:
        abort(403)
    error = request.args.get('error')
    return render_template("createactivity.html", error=error)

@app.route("/profile")
def profile():
    if not session["username"]:
        abort(403)
    success = request.args.get('success')
    if success:
        success = success.replace("-", " ")
        success = success.capitalize()
    error = request.args.get('error')
    if error:
        error = error.replace("-", " ")
        error = error.capitalize()
    return render_template("profile.html", success=success, error=error)

@app.route("/profile/delete")
def delete_profile():
    if not session["username"] and request.args.get('token') != session["csrf_token"]:
        abort(403)
    user = actions.find_user(session["username"])
    if user.is_creator:
        group = actions.get_user_group(session["username"])
        actions.delete_all_activities(group.id)
        actions.delete_all_members(group.id)
    else:
        actions.delete_pending_activities(user.id)
        actions.delete_user(user.id)
    del session["username"]
    del session["csrf_token"]
    return redirect("/")

@app.route("/login/post", methods=["POST"])
def login_post():
    username = request.form["username"]
    password = request.form["password"]
    if actions.check_login(username, password):
        session["username"] = username
        session["csrf_token"] = secrets.token_hex(16)
        return redirect("/")
    return redirect("/login?error=login-error")

@app.route("/signup/post", methods=["POST"])
def signup_post():
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
    session["csrf_token"] = secrets.token_hex(16)
    if group == "new":
        actions.create_user(username, password, True, True)
        return redirect(f"/group/create")
    actions.create_user(username, password, False, False, int(group))
    return redirect("/")

@app.route("/group/create/post", methods=["POST"])
def create_group_post():
    group_name = request.form["group-name"]
    username = session["username"]
    if not actions.user_can_create_group(username):
        abort(403)
    error = actions.check_group_name(group_name)
    if error:
        return redirect(f"/group/create?error={error}")
    group_id = actions.create_group(group_name)
    actions.add_user_to_group(username, group_id)
    return redirect("/")

@app.route("/activities/create/post", methods=["POST"])
def create_activity_post():
    if not session["username"] and request.form["csrf_token"] != session["csrf_token"]:
        abort(403)
    activity_name = request.form["activity-name"]
    error = actions.check_activity_name(activity_name)
    if error:
        return redirect(f"/activities/create?error={error}&activity={activity_name}")
    group = actions.get_user_group(session["username"])
    user = actions.find_user(session["username"])
    if not group:
        return redirect("/group/create")
    actions.create_activity(activity_name, group.id, user.id, user.is_admin)
    return redirect("/activities")

@app.route("/profile/changepassword", methods=["POST"])
def change_password():
    if not session["username"] and request.form["csrf_token"] != session["csrf_token"]:
        abort(403)
    current_password = request.form["current-password"]
    new_password = request.form["new-password"]
    new_password_again = request.form["new-password-again"]
    error = actions.check_password(new_password, new_password_again)
    if error:
        return redirect(f"/profile?error={error}")
    if actions.check_login(session["username"], current_password):
        actions.change_password(session["username"], new_password)
        return redirect("/profile?success=password-changed")
    return redirect("/profile?error=incorrect-password")

@app.errorhandler(403)
def forbidden(e):
    return render_template("403.html"), 403

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template("500.html", error=e.description), 500
