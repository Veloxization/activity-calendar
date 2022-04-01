from werkzeug.security import check_password_hash, generate_password_hash

class DBActions:
    def __init__(self, database):
        self.db = database

    def find_user(self, username):
        sql = "SELECT * FROM users WHERE username=:username"
        result = self.db.session.execute(sql, {"username": username})
        user = result.fetchone()
        return user

    def get_groups(self):
        sql = "SELECT * FROM groups"
        result = self.db.session.execute(sql)
        return result.fetchall()

    def find_group(self, group_name):
        sql = "SELECT * FROM groups WHERE group_name=:group_name"
        result = self.db.session.execute(sql, {"group_name": group_name})
        return result.fetchone()
    
    def create_user(self, username, password, is_admin, group_id):
        hash_value = generate_password_hash(password)
        sql = "INSERT INTO users (username, password, group_id, is_admin) VALUES (:username, :password, :group_id, :is_admin)"
        result = self.db.session.execute(sql, {"username": username, "password": hash_value, "group_id": group_id, "is_admin": is_admin})
        self.db.session.commit()

    def check_credentials(self, username, password):
        sql = "SELECT * FROM users WHERE username=:username"
        result = self.db.session.execute(sql, {"username": username})
        user = result.fetchone()
        if user:
            return check_password_hash(user.password, password)
        return False
