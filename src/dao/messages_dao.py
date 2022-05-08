class MessagesDAO:
    def __init__(self, database):
        self.db = database

    def get_messages_in_thread(self, thread_id):
        sql = "SELECT sender_id, recipient_id, (SELECT username FROM users WHERE users.id = messages.sender_id) AS sender_name, (SELECT username FROM users WHERE users.id = messages.recipient_id) AS recipient_name, time_sent, message_read, message FROM messages WHERE thread_id=:thread_id ORDER BY time_sent DESC"
        result = self.db.session.execute(sql, {"thread_id": thread_id})
        return result.fetchall()

    def get_user_message_threads(self, user_id):
        sql = "SELECT message_threads.id, message_threads.title, time_sent, (SELECT COUNT(*) FROM messages WHERE thread_id=message_threads.id AND recipient_id=:user_id AND NOT message_read) AS unread_count FROM messages INNER JOIN message_threads ON message_threads.id = thread_id WHERE sender_id=:user_id OR recipient_id=:user_id ORDER BY time_sent DESC"
        result = self.db.session.execute(sql, {"user_id": user_id})
        return result.fetchall()

    def count_unread_messages(self, user_id):
        sql = "SELECT COUNT(*) FROM messages WHERE recipient_id=:user_id AND NOT message_read"
        result = self.db.session.execute(sql, {"user_id": user_id})
        return result.fetchone().count

    def count_unread_messages_in_thread(self, thread_id, user_id):
        sql = "SELECT COUNT(*) FROM messages WHERE thread_id=:thread_id AND recipient_id=:user_id AND NOT message_read"
        result = self.db.session.execute(sql, {"thread_id": thread_id, "user_id": user_id})
        return result.fetchone().count

    def mark_thread_read(self, thread_id, user_id):
        sql = "UPDATE messages SET message_read=TRUE WHERE thread_id=:thread_id AND recipient_id=:user_id"
        self.db.session.execute(sql, {"thread_id": thread_id, "user_id": user_id})
        self.db.session.commit()

    def create_message(self, thread_id, sender_id, recipient_id, message_content):
        sql = "INSERT INTO messages (thread_id, message_read, sender_id, recipient_id, time_sent, message) VALUES (:thread_id, FALSE, :sender_id, :recipient_id, CURRENT_TIMESTAMP, :message_content)"
        self.db.session.execute(sql, {"thread_id": thread_id, "sender_id": sender_id, "recipient_id": recipient_id, "message_content": message_content})
        self.db.session.commit()
