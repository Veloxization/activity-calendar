CREATE TABLE groups (id SERIAL PRIMARY KEY, group_name VARCHAR(100));
CREATE TABLE users (id SERIAL PRIMARY KEY, username VARCHAR(20) UNIQUE, password TEXT, group_id INTEGER REFERENCES groups, is_admin BOOLEAN, is_creator BOOLEAN);
CREATE TABLE activities (id SERIAL PRIMARY KEY, activity VARCHAR(1000), group_id INTEGER REFERENCES groups, creator_id INTEGER REFERENCES users, is_approved BOOLEAN);
CREATE TABLE user_activities (id SERIAL PRIMARY KEY, user_id INTEGER REFERENCES users, activity_id INTEGER REFERENCES activities, start_time TIMESTAMP, end_time TIMESTAMP);
CREATE TABLE message_threads (id SERIAL PRIMARY KEY, title VARCHAR(256));
CREATE TABLE messages (id SERIAL PRIMARY KEY, thread_id INTEGER REFERENCES message_threads, message_read BOOLEAN, sender_id INTEGER REFERENCES users, recipient_id INTEGER REFERENCES users, time_sent TIMESTAMP, message VARCHAR(5000));