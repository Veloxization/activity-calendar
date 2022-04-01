CREATE TABLE users (id SERIAL PRIMARY KEY, username VARCHAR(20), password VARCHAR(64), group_id INTEGER REFERENCES groups, is_admin BOOLEAN);
CREATE TABLE groups (id SERIAL PRIMARY KEY, group_name VARCHAR(100));
CREATE TABLE activities (id SERIAL PRIMARY KEY, activity VARCHAR(1000), group_id INTEGER REFERENCES groups, is_approved BOOLEAN);
CREATE TABLE user_activities (id SERIAL PRIMARY KEY, user_id INTEGER REFERENCES users, activity_id INTEGER REFERENCES activities, start_time TIMESTAMP, end_time TIMESTAMP);
CREATE TABLE activity_goals (id SERIAL PRIMARY KEY, user_id INTEGER REFERENCES users, activity_id INTEGER REFERENCES activities, start_time TIMESTAMP, end_time TIMESTAMP);
CREATE TABLE messages (id SERIAL PRIMARY KEY, sender_id INTEGER REFERENCES users, recipient_id INTEGER REFERENCES users, message VARCHAR(5000));