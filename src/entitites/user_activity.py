from src.dao.user_activities_dao import UserActivitiesDAO

class UserActivity:
    def __init__(self, database):
        self.dao = UserActivitiesDAO(database)

    def get_user_activity(self, username):
        return self.dao.get_user_activity(username)