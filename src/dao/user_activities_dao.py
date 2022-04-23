from src.dao.users_dao import UsersDAO

class UserActivitiesDAO:
    def __init__(self, database):
        self.db = database

    def get_user_activity(self, username):
        user = UsersDAO(self.db).find_user(username)
        if not user:
            return None
        sql = "SELECT * FROM user_activities WHERE user_id=:user_id AND end_time=NULL"
        result = self.db.session.execute(sql, {"user_id": user.id})
        return result.fetchone()