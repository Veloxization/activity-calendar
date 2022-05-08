from src.dao.message_threads_dao import MessageThreadsDAO

class MessageThread:
    def __init__(self, database):
        self.dao = MessageThreadsDAO(database)

    def get_message_thread(self, thread_id):
        return self.dao.get_message_thread(thread_id)

    def create_message_thread(self, thread_name):
        return self.dao.create_message_thread(thread_name)

    def delete_thread(self, thread_id):
        self.dao.delete_thread(thread_id)
