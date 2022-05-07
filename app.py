from flask import Flask, render_template, redirect, request, session, abort
from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy import functools
from src.entitites.user import User
from src.entitites.group import Group
from src.entitites.activity import Activity
from src.entitites.user_activity import UserActivity
from os import getenv
import secrets

app = Flask(__name__, static_url_path='')
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URI")
app.secret_key = getenv("SECRET_KEY")
db = SQLAlchemy(app)
user_entity = User(db)
group_entity = Group(db)
activity_entity = Activity(db)
user_activity_entity = UserActivity(db)

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
    groups = group_entity.get_groups()
    error = request.args.get('error')
    if error:
        error = error.replace("-", " ")
        error = error.capitalize()
    return render_template("signup.html", groups=groups, error=error)

@app.route("/group")
def group():
    if not session["username"]:
        abort(403)
    group = group_entity.get_user_group(session["username"])
    if group is None:
        return redirect("/group/create")
    member_count = len(user_entity.get_group_members(group.id))
    admins = user_entity.get_group_admins(group.id)
    members = user_entity.get_group_regular_members(group.id)
    return render_template("group.html", group=group, member_count=member_count, admins=admins, members=members)

@app.route("/group/create")
def create_group():
    if not session["username"]:
        abort(403)
    if not user_entity.user_can_create_group(session["username"]):
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
    user_activity = user_activity_entity.get_user_activity(session["username"])
    if user_activity:
        active = activity_entity.get_activity(user_activity.activity_id)
    else:
        active = None
    group = group_entity.get_user_group(session["username"])
    if not group:
        return redirect("/group/create")
    user = user_entity.find_user(session["username"])
    activities = activity_entity.get_group_activities(group.id)
    return render_template("activities.html", active=active, user_activity=user_activity, activity_count=len(activities), user=user, activities=activities)

@app.route("/activities/create")
def create_activity():
    if not session["username"]:
        abort(403)
    error = request.args.get('error')
    return render_template("createactivity.html", error=error)

@app.route("/activities/start")
def start_activity():
    if not session["username"] or request.args.get('token') != session["csrf_token"]:
        abort(403)
    user_id = user_entity.find_user(session["username"]).id
    activity_id = int(request.args.get('activity'))
    user_activity_entity.create_user_activity(user_id, activity_id)
    return redirect("/activities")

@app.route("/activities/stop")
def stop_activity():
    if not session["username"] or request.args.get('token') != session["csrf_token"]:
        abort(403)
    user_id = user_entity.find_user(session["username"]).id
    user_activity_entity.end_user_activity(user_id)
    activity_id = request.args.get('start')
    if activity_id:
        user_activity_entity.create_user_activity(user_id, int(activity_id))
    return redirect("/activities")

@app.route("/activities/manage")
def manage_activity():
    if not session["username"]:
        abort(403)
    user = user_entity.find_user(session["username"])
    activity_id = int(request.args.get('activity'))
    activity = activity_entity.get_activity(activity_id)
    suggestion_user = user_entity.get_user(activity.creator_id)
    activity_name = request.args.get('activity-name')
    if not (user.is_admin or activity.creator_id == user.id):
        abort(403)
    return render_template("manageactivity.html", activity=activity, activity_name=activity_name, suggestion_user=suggestion_user)

@app.route("/activities/approve")
def approve_activity():
    if not session["username"] or request.args.get('token') != session["csrf_token"]:
        abort(403)
    user = user_entity.find_user(session["username"])
    if not user.is_admin:
        abort(403)
    activity = activity_entity.get_activity(int(request.args.get('activity')))
    creator = user_entity.get_group_creator(activity.group_id)
    activity_entity.approve_pending_activity(activity.id, creator.id)
    return redirect("/activities")

@app.route("/activities/delete")
def delete_activity():
    if not session["username"] or request.args.get('token') != session["csrf_token"]:
        abort(403)
    activity_id = int(request.args.get('activity'))
    activity = activity_entity.get_activity(activity_id)
    user = user_entity.find_user(session["username"])
    if not (user.is_admin or activity.creator_id == user.id):
        abort(403)
    user_activity_entity.end_all_activity_instances(activity_id)
    user_activity_entity.clear_activity_reference(activity_id)
    activity_entity.delete_activity(activity_id)
    return redirect("/activities")

@app.route("/profile")
def profile():
    if not session["username"]:
        abort(403)
    profile_user = user_entity.find_user(request.args.get('username'))
    if not profile_user:
        abort(404)
    client_user = user_entity.find_user(session["username"])
    if client_user.group_id != profile_user.group_id:
        abort(403)
    current_activity = user_activity_entity.get_user_activity(profile_user.username)
    user_activities = user_activity_entity.get_user_activities(profile_user.username)
    deleted_activities = user_activity_entity.get_deleted_user_activities(profile_user.username)
    return render_template("profile.html", user=profile_user, current_activity=current_activity, user_activities=user_activities, client_user=client_user, deleted_activities=deleted_activities)

@app.route("/profile/settings")
def profile_settings():
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
    return render_template("profilesettings.html", success=success, error=error)

@app.route("/profile/delete")
def delete_profile():
    if not session["username"] or request.args.get('token') != session["csrf_token"]:
        abort(403)
    user = user_entity.find_user(session["username"])
    user_activity_entity.delete_user_activities(user.id)
    if user.is_creator:
        group = group_entity.get_user_group(session["username"])
        user_activity_entity.delete_group_user_activities(group.id)
        activity_entity.delete_all_activities(group.id)
        user_entity.delete_all_members(group.id)
        group_entity.delete_group(group.id)
    else:
        activity_entity.delete_pending_activities(user.id)
        user_entity.delete_user(user.id)
    del session["username"]
    del session["csrf_token"]
    return redirect("/")

@app.route("/login/post", methods=["POST"])
def login_post():
    username = request.form["username"]
    password = request.form["password"]
    if user_entity.check_login(username, password):
        session["username"] = username
        session["csrf_token"] = secrets.token_hex(16)
        return redirect("/")
    return redirect(f"/login?error=login-error&username={username}")

@app.route("/signup/post", methods=["POST"])
def signup_post():
    username = request.form["username"]
    password = request.form["password"]
    password_again = request.form["password-again"]
    group = request.form["group"]
    form_input = f"username={username}&group={group}"
    username_error = user_entity.check_username(username)
    if username_error:
        return redirect(f"/signup?error={username_error}&{form_input}")
    password_error = user_entity.check_password(password, password_again)
    if password_error:
        return redirect(f"/signup?error={password_error}&{form_input}")
    session["username"] = username
    session["csrf_token"] = secrets.token_hex(16)
    if group == "new":
        user_entity.create_user(username, password, True, True)
        return redirect(f"/group/create")
    user_entity.create_user(username, password, False, False, int(group))
    return redirect("/")

@app.route("/group/create/post", methods=["POST"])
def create_group_post():
    group_name = request.form["group-name"]
    username = session["username"]
    if not user_entity.user_can_create_group(username):
        abort(403)
    error = group_entity.check_group_name(group_name)
    if error:
        return redirect(f"/group/create?error={error}")
    group_id = group_entity.create_group(group_name)
    user_entity.add_user_to_group(username, group_id)
    return redirect("/")

@app.route("/activities/create/post", methods=["POST"])
def create_activity_post():
    if not session["username"] or request.form["csrf_token"] != session["csrf_token"]:
        abort(403)
    activity_name = request.form["activity-name"]
    error = activity_entity.check_activity_name(activity_name)
    if error:
        return redirect(f"/activities/create?error={error}&activity={activity_name}")
    group = group_entity.get_user_group(session["username"])
    user = user_entity.find_user(session["username"])
    if not group:
        return redirect("/group/create")
    activity_entity.create_activity(activity_name, group.id, user.id, user.is_admin)
    return redirect("/activities")

@app.route("/activities/manage/post", methods=["POST"])
def manage_activity_post():
    if not session["username"] or request.form["csrf_token"] != session["csrf_token"]:
        abort(403)
    activity_name = request.form["activity-name"]
    activity_id = int(request.form["activity-id"])
    user = user_entity.find_user(session["username"])
    activity = activity_entity.get_activity(activity_id)
    if not (user.is_admin or user.id == activity.creator_id):
        abort(403)
    error = activity_entity.check_activity_name(activity_name)
    if error:
        return redirect(f"/activities/manage?activity={activity_id}&error={error}&activity-name={activity_name}")
    activity_entity.set_activity_name(activity_id, activity_name)
    return redirect(f"/activities/manage?activity={activity_id}")

@app.route("/profile/changepassword", methods=["POST"])
def change_password():
    if not session["username"] or request.form["csrf_token"] != session["csrf_token"]:
        abort(403)
    current_password = request.form["current-password"]
    new_password = request.form["new-password"]
    new_password_again = request.form["new-password-again"]
    error = user_entity.check_password(new_password, new_password_again)
    if error:
        return redirect(f"/profile?error={error}")
    if user_entity.check_login(session["username"], current_password):
        user_entity.change_password(session["username"], new_password)
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
