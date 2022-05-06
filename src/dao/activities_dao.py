class ActivitiesDAO:
    def __init__(self, database):
        self.db = database

    def create_activity(self, activity_name, group_id, creator_id, is_approved=False):
        sql = "INSERT INTO activities (activity, group_id, creator_id, is_approved) VALUES (:activity_name, :group_id, :creator_id, :is_approved)"
        result = self.db.session.execute(sql, {"activity_name": activity_name, "group_id": group_id, "creator_id": creator_id, "is_approved": is_approved})
        self.db.session.commit()

    def get_activity(self, activity_id):
        sql = "SELECT * FROM activities WHERE id=:activity_id"
        result = self.db.session.execute(sql, {"activity_id": activity_id})
        return result.fetchone()
    
    def get_group_activities(self, group_id):
        sql = "SELECT * FROM activities WHERE group_id=:group_id ORDER BY activity ASC"
        result = self.db.session.execute(sql, {"group_id": group_id})
        return result.fetchall()

    def set_activity_name(self, activity_id, activity_name):
        sql = "UPDATE activities SET activity=:activity_name WHERE id=:activity_id"
        self.db.session.execute(sql, {"activity_name": activity_name, "activity_id": activity_id})
        self.db.session.commit()

    def delete_pending_activities(self, user_id):
        sql = "DELETE FROM activities WHERE creator_id=:user_id"
        result = self.db.session.execute(sql, {"user_id": user_id})
        self.db.session.commit()

    def delete_all_activities(self, group_id):
        sql = "DELETE FROM activities WHERE group_id=:group_id"
        result = self.db.session.execute(sql, {"group_id": group_id})
        self.db.session.commit()

    def delete_activity(self, activity_id):
        sql = "DELETE FROM activities WHERE id=:activity_id"
        self.db.session.execute(sql, {"activity_id": activity_id})
        self.db.session.commit()