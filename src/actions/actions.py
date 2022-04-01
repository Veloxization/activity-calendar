from src.actions.dbactions import DBActions

class Actions:
    def __init__(self, database):
        self.db_action = DBActions(database)

    def username_taken(self, username):
        user = self.db_action.find_user(username)
        return user is not None

    def get_groups(self):
        return self.db_action.get_groups()

    def check_group_name(self, group_name):
        if self.group_name_taken(group_name):
            return "group-name-taken"
        if len(group_name) < 3:
            return "group-name-too-short"
        if len(group_name) > 100:
            return "group-name-too-long"
        return None

    def group_name_taken(self, group_name):
        group = self.db_action.find_group(group_name)
        return group is not None

    def check_username(self, username):
        if self.username_taken(username):
            return "username-taken"
        if len(username) < 3:
            return "username-too-short"
        if len(username) > 20:
            return "username-too-long"
        if not username.isalnum():
            return "username-has-forbidden-characters"
        return None

    def check_password(self, password, password_again):
        if password != password_again:
            return "passwords-not-matching"
        if len(password) < 8:
            return "password-too-short"
        if len(password) > 64:
            return "password-too-long"
        if ' ' in password:
            return "password-has-forbidden-characters"
        return None

    def user_can_create_group(self, username):
        user = self.db_action.find_user(username)
        if not user:
            return False
        return user.group_id is None and user.is_admin

    def create_user(self, username, password, is_admin, group_id=None):
        self.db_action.create_user(username, password, is_admin, group_id)

    def check_login(self, username, password):
        return self.db_action.check_credentials(username, password)

    def add_user_to_group(self, username, group_id):
        self.db_action.change_user_group(username, group_id)

    def create_group(self, group_name):
        return self.db_action.create_group(group_name)
