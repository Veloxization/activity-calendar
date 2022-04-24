from src.dao.users_dao import UsersDAO

class User:
    def __init__(self, database):
        self.dao = UsersDAO(database)

    def username_taken(self, username):
        user = self.dao.find_user(username)
        return user is not None

    def find_user(self, username):
        return self.dao.find_user(username)

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
        user = self.dao.find_user(username)
        if not user:
            return False
        return user.group_id is None and user.is_admin

    def create_user(self, username, password, is_admin, is_creator, group_id=None):
        self.dao.create_user(username, password, is_admin, is_creator, group_id)

    def check_login(self, username, password):
        return self.dao.check_credentials(username, password)

    def add_user_to_group(self, username, group_id):
        self.dao.change_user_group(username, group_id)

    def change_password(self, username, password):
        self.dao.change_password(username, password)

    def get_user(self, user_id):
        return self.dao.get_user(user_id)

    def get_user_group(self, username):
        return self.dao.get_user_group(username)

    def get_group_admins(self, group_id):
        return self.dao.get_group_admins(group_id)

    def get_group_regular_members(self, group_id):
        return self.dao.get_group_regular_members(group_id)

    def get_group_members(self, group_id):
        return self.dao.get_group_members(group_id)

    def is_admin(self, username):
        user = self.dao.find_user(username)
        if not user:
            return False
        return user.is_admin

    def delete_user(self, user_id):
        self.dao.delete_user(user_id)

    def delete_all_members(self, group_id):
        self.dao.delete_all_members(group_id)
