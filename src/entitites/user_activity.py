from src.dao.user_activities_dao import UserActivitiesDAO

class UserActivity:
    def __init__(self, database):
        self.dao = UserActivitiesDAO(database)

    def get_user_activity(self, username):
        return self.dao.get_user_activity(username)

    def get_user_activities(self, username):
        return self.dao.get_user_activities(username)

    def get_deleted_user_activities(self, username):
        return self.dao.get_deleted_user_activities(username)

    def create_user_activity(self, user_id, activity_id):
        self.dao.create_user_activity(user_id, activity_id)

    def end_user_activity(self, user_id):
        self.dao.end_user_activity(user_id)

    def end_all_activity_instances(self, activity_id):
        self.dao.end_all_activity_instances(activity_id)

    def start_new_user_activity(self, user_id, activity_id):
        self.end_user_activity(user_id)
        self.start_new_user_activity(user_id, activity_id)

    def clear_activity_reference(self, activity_id):
        self.dao.clear_activity_reference(activity_id)

    def delete_user_activities(self, user_id):
        self.dao.delete_user_activities(user_id)

    def delete_group_user_activities(self, group_id):
        self.dao.delete_group_user_activities(group_id)