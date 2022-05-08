class MessagesDAO:
    def __init__(self, database):
        self.db = database

    def get_messages_in_thread(self, thread_id):
        sql = "SELECT * FROM messages WHERE thread_id=:thread_id ORDER BY time_sent DESC"
        self.db.session.execute(sql, {"thread_id": thread_id})
        return self.db.session.fetchall()

    def get_user_message_threads(self, user_id):
        sql = "SELECT message_threads.id, message_threads.title FROM messages INNER JOIN message_threads ON message_threads.id = thread_id WHERE sender_id=:user_id OR recipient_id=:user_id ORDER BY time_sent DESC"
        self.db.session.execute(sql, {"user_id": user_id})
        return self.db.session.fetchall()

    def count_unread_messages(self, user_id):
        sql = "SELECT COUNT(*) FROM messages WHERE recipient_id=:user_id AND NOT message_read"
        self.db.session.execute(sql, {"user_id": user_id})
        return self.db.session.fetchone().count

    def count_unread_messages_in_thread(self, thread_id, user_id):
        sql = "SELECT COUNT(*) FROM messages WHERE thread_id=:thread_id AND recipient_id=:user_id AND NOT message_read"
        self.db.session.execute(sql, {"thread_id": thread_id, "user_id": user_id})
        return self.db.session.fetchone().count

    def mark_thread_read(self, thread_id, user_id):
        sql = "UPDATE messages SET message_read=TRUE WHERE thread_id=:thread_id AND recipient_id=:user_id"
        self.db.session.execute(sql, {"thread_id": thread_id, "user_id": user_id})
        self.db.session.commit()

    def create_message(self, thread_id, sender_id, recipient_id, message_content):
        sql = "INSERT INTO messages (thread_id, message_read, sender_id, recipient_id, time_sent, message) VALUES (:thread_id, FALSE, :sender_id, :recipient_id, CURRENT_TIMESTAMP, :message_content"
        self.db.session.execute(sql, {"thread_id": thread_id, "sender_id": sender_id, "recipient_id": recipient_id, "message_content": message_content})
        self.db.session.commit()
