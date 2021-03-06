from src.dao.messages_dao import MessagesDAO

class Message:
    def __init__(self, database):
        self.dao = MessagesDAO(database)

    def get_messages_in_thread(self, thread_id):
        return self.dao.get_messages_in_thread(thread_id)

    def get_user_message_threads(self, user_id):
        # Couldn't get this working through DISTINCT, GROUP BY etc. so I'll do it like this
        # Not the most elegant solution but it works...
        threads = self.dao.get_user_message_threads(user_id)
        unique_threads = []
        seen_threads = set()
        for thread in threads:
            if thread.id not in seen_threads:
                unique_threads.append(thread)
            seen_threads.add(thread.id)
        return unique_threads

    def count_unread_messages(self, user_id):
        return self.dao.count_unread_messages(user_id)

    def mark_thread_read(self, thread_id, user_id):
        self.dao.mark_thread_read(thread_id, user_id)

    def create_message(self, thread_id, sender_id, recipient_id, message_content):
        self.dao.create_message(thread_id, sender_id, recipient_id, message_content)

    def delete_user_messages(self, user_id):
        return self.dao.delete_user_messages(user_id)
