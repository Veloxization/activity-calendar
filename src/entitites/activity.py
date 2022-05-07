from src.dao.activities_dao import ActivitiesDAO

class Activity:
    def __init__(self, database):
        self.dao = ActivitiesDAO(database)

    def check_activity_name(self, activity_name):
        if len(activity_name) < 1:
            return "name-too-short"
        if len(activity_name) > 1000:
            return "name-too-long"
        return None

    def create_activity(self, activity_name, group_id, creator_id, is_approved=False):
        self.dao.create_activity(activity_name, group_id, creator_id, is_approved)

    def get_activity(self, activity_id):
        return self.dao.get_activity(activity_id)

    def get_group_activities(self, group_id):
        return self.dao.get_group_activities(group_id)

    def set_activity_name(self, activity_id, activity_name):
        self.dao.set_activity_name(activity_id, activity_name)

    def approve_pending_activity(self, activity_id, group_creator_id):
        self.dao.approve_pending_activity(activity_id, group_creator_id)

    def delete_pending_activities(self, user_id):
        self.dao.delete_pending_activities(user_id)

    def delete_all_activities(self, group_id):
        self.dao.delete_all_activities(group_id)

    def delete_activity(self, activity_id):
        self.dao.delete_activity(activity_id)
