from src.dao.groups_dao import GroupsDAO

class Group:
    def __init__(self, database):
        self.dao = GroupsDAO(database)

    def get_groups(self):
        return self.dao.get_groups()

    def check_group_name(self, group_name):
        if self.group_name_taken(group_name):
            return "group-name-taken"
        if len(group_name) < 3:
            return "group-name-too-short"
        if len(group_name) > 100:
            return "group-name-too-long"
        return None

    def group_name_taken(self, group_name):
        group = self.dao.find_group(group_name)
        return group is not None

    def create_group(self, group_name):
        return self.dao.create_group(group_name)

    def get_user_group(self, username):
        return self.dao.get_user_group(username)

    def delete_group(self, group_id):
        self.dao.delete_group(group_id)
