from werkzeug.security import check_password_hash, generate_password_hash

class DBActions:
    def __init__(self, database):
        self.db = database

    def find_user(self, username):
        sql = "SELECT * FROM users WHERE LOWER(username)=LOWER(:username)"
        result = self.db.session.execute(sql, {"username": username})
        user = result.fetchone()
        return user

    def get_groups(self):
        sql = "SELECT * FROM groups ORDER BY group_name ASC"
        result = self.db.session.execute(sql)
        return result.fetchall()

    def find_group(self, group_name):
        sql = "SELECT * FROM groups WHERE LOWER(group_name)=LOWER(:group_name)"
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

    def change_user_group(self, username, group_id):
        sql = "UPDATE users SET group_id=:group_id WHERE username=:username"
        result = self.db.session.execute(sql, {"group_id": group_id, "username": username})
        self.db.session.commit()

    def create_group(self, group_name):
        sql = "INSERT INTO groups (group_name) VALUES (:group_name)"
        result = self.db.session.execute(sql, {"group_name": group_name})
        self.db.session.commit()
        sql = "SELECT id FROM groups WHERE group_name=:group_name"
        result = self.db.session.execute(sql, {"group_name": group_name})
        return result.fetchone().id

    def create_activity(self, activity_name, group_id, creator_id, is_approved=False):
        sql = "INSERT INTO activities (activity, group_id, creator_id, is_approved) VALUES (:activity_name, :group_id, :creator_id, :is_approved)"
        result = self.db.session.execute(sql, {"activity_name": activity_name, "group_id": group_id, "creator_id": creator_id, "is_approved": is_approved})
        self.db.session.commit()

    def get_user_group(self, username):
        user = self.find_user(username)
        if not user:
            return None
        sql = "SELECT * FROM groups WHERE id=:group_id"
        result = self.db.session.execute(sql, {"group_id": user.group_id})
        return result.fetchone()

    def get_group_admins(self, group_id):
        sql = "SELECT * FROM users WHERE group_id=:group_id AND is_admin ORDER BY username ASC"
        result = self.db.session.execute(sql, {"group_id": group_id})
        return result.fetchall()

    def get_group_regular_members(self, group_id):
        sql = "SELECT * FROM users WHERE group_id=:group_id AND is_admin='no' ORDER BY username ASC"
        result = self.db.session.execute(sql, {"group_id": group_id})
        return result.fetchall()

    def get_group_members(self, group_id):
        sql = "SELECT * FROM users WHERE group_id=:group_id ORDER BY username ASC"
        result = self.db.session.execute(sql, {"group_id": group_id})
        return result.fetchall()

    def get_user_activity(self, username):
        user = self.find_user(username)
        if not user:
            return None
        sql = "SELECT * FROM user_activities WHERE user_id=:user_id AND end_time=NULL"
        result = self.db.session.execute(sql, {"user_id": user.id})
        return result.fetchone()

    def get_activity(self, activity_id):
        sql = "SELECT * FROM activities WHERE id=:activity_id"
        result = self.db.session.execute(sql, {"activity_id": activity_id})
        return result.fetchone()

    def get_group_activities(self, group_id):
        sql = "SELECT * FROM activities WHERE group_id=:group_id ORDER BY activity ASC"
        result = self.db.session.execute(sql, {"group_id": group_id})
        return result.fetchall()
