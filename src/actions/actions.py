from src.actions.dbactions import DBActions

class Actions:
    def __init__(self, database):
        self.db_action = DBActions(database)

    def username_taken(self, username):
        user = self.db_action.find_user(username)
        return user is not None

    def get_groups(self):
        return self.db_action.get_groups()