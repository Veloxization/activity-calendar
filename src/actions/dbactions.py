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