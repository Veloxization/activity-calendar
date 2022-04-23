from src.dao.users_dao import UsersDAO

class UserActivitiesDAO:
    def __init__(self, database):
        self.db = database

    def get_user_activity(self, username):
        user = UsersDAO(self.db).find_user(username)
        if not user:
            return None
        sql = "SELECT * FROM user_activities WHERE user_id=:user_id AND end_time IS NULL"
        result = self.db.session.execute(sql, {"user_id": user.id})
        return result.fetchone()

    def create_user_activity(self, user_id, activity_id):
        sql = "INSERT INTO user_activities (user_id, activity_id, start_time) VALUES (:user_id, :activity_id, CURRENT_TIMESTAMP)"
        self.db.session.execute(sql, {"user_id": user_id, "activity_id": activity_id})
        self.db.session.commit()

    def end_user_activity(self, user_id):
        sql = "UPDATE user_activities SET end_time=CURRENT_TIMESTAMP WHERE user_id=:user_id AND end_time IS NULL"
        self.db.session.execute(sql, {"user_id": user_id})
        self.db.session.commit()
