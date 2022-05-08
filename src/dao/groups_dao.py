from src.dao.users_dao import UsersDAO

class GroupsDAO:
    def __init__(self, database):
        self.db = database

    def get_groups(self):
        sql = "SELECT groups.id, group_name FROM groups ORDER BY group_name ASC"
        result = self.db.session.execute(sql)
        return result.fetchall()

    def find_group(self, group_name):
        sql = "SELECT groups.id, group_name FROM groups WHERE LOWER(group_name)=LOWER(:group_name)"
        result = self.db.session.execute(sql, {"group_name": group_name})
        return result.fetchone()

    def create_group(self, group_name):
        sql = "INSERT INTO groups (group_name) VALUES (:group_name) RETURNING id"
        result = self.db.session.execute(sql, {"group_name": group_name})
        self.db.session.commit()
        return result.fetchone().id

    def get_user_group(self, username):
        user = UsersDAO(self.db).find_user(username)
        if not user:
            return None
        sql = "SELECT groups.id, group_name FROM groups WHERE id=:group_id"
        result = self.db.session.execute(sql, {"group_id": user.group_id})
        return result.fetchone()

    def delete_group(self, group_id):
        sql = "DELETE FROM groups WHERE id=:group_id"
        self.db.session.execute(sql, {"group_id": group_id})
        self.db.session.commit()
    