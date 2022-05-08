class MessageThreadsDAO:
    def __init__(self, database):
        self.db = database

    def get_message_thread(self, thread_id):
        sql = "SELECT message_threads.id, title FROM message_threads WHERE id=:thread_id"
        result = self.db.session.execute(sql, {"thread_id": thread_id})
        return result.fetchone()

    def create_message_thread(self, thread_name):
        sql = "INSERT INTO message_threads (title) VALUES (:thread_name) RETURNING *"
        result = self.db.session.execute(sql, {"thread_name": thread_name})
        self.db.session.commit()
        return result.fetchone()

    def delete_thread(self, thread_id):
        sql = "DELETE FROM message_threads WHERE id=:thread_id"
        self.db.session.execute(sql, {"thread_id": thread_id})
        self.db.session.commit()
