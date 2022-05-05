from src.dao.users_dao import UsersDAO

class UserActivitiesDAO:
    def __init__(self, database):
        self.db = database

    def get_user_activity(self, username):
        sql = "SELECT * FROM user_activities INNER JOIN users ON user_id=users.id WHERE users.username=:username AND end_time IS NULL"
        result = self.db.session.execute(sql, {"username": username})
        return result.fetchone()

    def create_user_activity(self, user_id, activity_id):
        sql = "INSERT INTO user_activities (user_id, activity_id, start_time) VALUES (:user_id, :activity_id, CURRENT_TIMESTAMP)"
        self.db.session.execute(sql, {"user_id": user_id, "activity_id": activity_id})
        self.db.session.commit()

    def end_user_activity(self, user_id):
        sql = "UPDATE user_activities SET end_time=CURRENT_TIMESTAMP WHERE user_id=:user_id AND end_time IS NULL"
        self.db.session.execute(sql, {"user_id": user_id})
        self.db.session.commit()

    def clear_activity_reference(self, activity_id):
        sql = "UPDATE user_activities SET activity_id=NULL WHERE activity_id=:activity_id"
        self.db.session.execute(sql, {"activity_id": activity_id})
        self.db.session.commit()

    def delete_user_activities(self, user_id):
        sql = "DELETE FROM user_activities WHERE user_id=:user_id"
        self.db.session.execute(sql, {"user_id": user_id})
        self.db.session.commit()

    def delete_group_user_activities(self, group_id):
        sql = "DELETE FROM user_activities USING activities WHERE activities.id=activity_id AND activities.group_id=:group_id"
        self.db.session.execute(sql, {"group_id": group_id})
        sql = "DELETE FROM user_activities USING users WHERE users.id=user_id AND users.group_id=:group_id"
        self.db.session.execute(sql, {"group_id": group_id})
        self.db.session.commit()
