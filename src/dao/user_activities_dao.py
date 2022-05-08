class UserActivitiesDAO:
    def __init__(self, database):
        self.db = database

    def get_user_activity(self, username):
        sql = "SELECT user_activities.id, user_id, activity_id, start_time, end_time FROM user_activities INNER JOIN users ON user_id=users.id INNER JOIN activities ON activity_id=activities.id WHERE users.username=:username AND end_time IS NULL"
        result = self.db.session.execute(sql, {"username": username})
        return result.fetchone()

    def get_user_activities(self, username):
        sql = "SELECT user_activities.id, user_id, activity_id, start_time, end_time FROM user_activities INNER JOIN users ON user_id=users.id INNER JOIN activities ON activity_id=activities.id WHERE users.username=:username ORDER BY start_time DESC"
        result = self.db.session.execute(sql, {"username": username})
        return result.fetchall()

    def get_deleted_user_activities(self, username):
        sql = "SELECT user_activities.id, user_id, activity_id, start_time, end_time FROM user_activities INNER JOIN users ON user_id=users.id WHERE users.username=:username AND activity_id IS NULL ORDER BY start_time DESC"
        result = self.db.session.execute(sql, {"username": username})
        return result.fetchall()

    def create_user_activity(self, user_id, activity_id):
        sql = "INSERT INTO user_activities (user_id, activity_id, start_time) VALUES (:user_id, :activity_id, CURRENT_TIMESTAMP)"
        self.db.session.execute(sql, {"user_id": user_id, "activity_id": activity_id})
        self.db.session.commit()

    def end_user_activity(self, user_id):
        sql = "UPDATE user_activities SET end_time=CURRENT_TIMESTAMP WHERE user_id=:user_id AND end_time IS NULL"
        self.db.session.execute(sql, {"user_id": user_id})
        self.db.session.commit()

    def end_all_activity_instances(self, activity_id):
        sql = "UPDATE user_activities SET end_time=CURRENT_TIMESTAMP WHERE activity_id=:activity_id"
        self.db.session.execute(sql, {"activity_id": activity_id})
        self.db.session.commit()

    def end_pending_activity_instances(self, user_id):
        sql = "UPDATE user_activities SET end_time=CURRENT_TIMESTAMP FROM activities WHERE activity_id=activities.id AND activities.creator_id=:user_id"
        self.db.session.execute(sql, {"user_id": user_id})
        self.db.session.commit()

    def clear_activity_reference(self, activity_id):
        sql = "UPDATE user_activities SET activity_id=NULL WHERE activity_id=:activity_id"
        self.db.session.execute(sql, {"activity_id": activity_id})
        self.db.session.commit()

    def clear_pending_activity_references(self, user_id):
        sql = "UPDATE user_activities SET activity_id=NULL FROM activities WHERE activity_id=activities.id AND activities.creator_id=:user_id"
        self.db.session.execute(sql, {"user_id": user_id})
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
