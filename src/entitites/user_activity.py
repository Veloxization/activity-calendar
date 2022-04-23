from src.dao.user_activities_dao import UserActivitiesDAO

class UserActivity:
    def __init__(self, database):
        self.dao = UserActivitiesDAO(database)

    def get_user_activity(self, username):
        return self.dao.get_user_activity(username)

    def create_user_activity(self, user_id, activity_id):
        self.dao.create_user_activity(user_id, activity_id)

    def end_user_activity(self, user_id):
        self.dao.end_user_activity(user_id)

    def start_new_user_activity(self, user_id, activity_id):
        self.end_user_activity(user_id)
        self.start_new_user_activity(user_id, activity_id)