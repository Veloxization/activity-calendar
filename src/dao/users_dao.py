from werkzeug.security import check_password_hash, generate_password_hash

class UsersDAO:
    def __init__(self, database):
        self.db = database

    def find_user(self, username):
        sql = "SELECT * FROM users WHERE LOWER(username)=LOWER(:username)"
        result = self.db.session.execute(sql, {"username": username})
        user = result.fetchone()
        return user

    def create_user(self, username, password, is_admin, is_creator, group_id):
        hash_value = generate_password_hash(password)
        sql = "INSERT INTO users (username, password, group_id, is_admin, is_creator) VALUES (:username, :password, :group_id, :is_admin, :is_creator)"
        result = self.db.session.execute(sql, {"username": username, "password": hash_value, "group_id": group_id, "is_admin": is_admin, "is_creator": is_creator})
        self.db.session.commit()

    def check_credentials(self, username, password):
        sql = "SELECT * FROM users WHERE username=:username"
        result = self.db.session.execute(sql, {"username": username})
        user = result.fetchone()
        if user:
            return check_password_hash(user.password, password)
        return False

    def change_user_group(self, username, group_id):
        sql = "UPDATE users SET group_id=:group_id WHERE username=:username"
        result = self.db.session.execute(sql, {"group_id": group_id, "username": username})
        self.db.session.commit()

    def change_password(self, username, password):
        user = self.find_user(username)
        if not user:
            return
        hash_value = generate_password_hash(password)
        sql = "UPDATE users SET password=:password WHERE id=:user_id"
        result = self.db.session.execute(sql, {"password": hash_value, "user_id": user.id})
        self.db.session.commit()

    def get_user(self, user_id):
        sql = "SELECT * FROM users WHERE id=:user_id"
        result = self.db.session.execute(sql, {"user_id": user_id})
        return result.fetchone()

    def get_group_admins(self, group_id):
        sql = "SELECT * FROM users WHERE group_id=:group_id AND is_admin ORDER BY username ASC"
        result = self.db.session.execute(sql, {"group_id": group_id})
        return result.fetchall()

    def get_group_creator(self, group_id):
        sql = "SELECT * FROM users WHERE group_id=:group_id AND is_creator=TRUE"
        result = self.db.session.execute(sql, {"group_id": group_id})
        return result.fetchone()

    def get_group_regular_members(self, group_id):
        sql = "SELECT * FROM users WHERE group_id=:group_id AND is_admin='no' ORDER BY username ASC"
        result = self.db.session.execute(sql, {"group_id": group_id})
        return result.fetchall()

    def get_group_members(self, group_id):
        sql = "SELECT * FROM users WHERE group_id=:group_id ORDER BY username ASC"
        result = self.db.session.execute(sql, {"group_id": group_id})
        return result.fetchall()

    def get_group_members_except(self, group_id, user_id):
        sql = "SELECT * FROM users WHERE group_id=:group_id AND id!=:user_id ORDER BY username ASC"
        result = self.db.session.execute(sql, {"group_id": group_id, "user_id": user_id})
        return result.fetchall()

    def make_admin(self, user_id):
        sql = "UPDATE users SET is_admin=TRUE WHERE id=:user_id"
        self.db.session.execute(sql, {"user_id": user_id})
        self.db.session.commit()

    def make_member(self, user_id):
        sql = "UPDATE users SET is_admin=FALSE WHERE id=:user_id"
        self.db.session.execute(sql, {"user_id": user_id})
        self.db.session.commit()

    def delete_user(self, user_id):
        sql = "DELETE FROM users WHERE id=:user_id"
        result = self.db.session.execute(sql, {"user_id": user_id})
        self.db.session.commit()

    def delete_all_members(self, group_id):
        sql = "DELETE FROM users WHERE group_id=:group_id"
        result = self.db.session.execute(sql, {"group_id": group_id})
        self.db.session.commit()