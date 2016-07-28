import sqlite3
import uuid

connection = sqlite3.connect('pointsboost.db', check_same_thread=False)


def initialize():
    cursor = connection.cursor()
    cursor.execute(''' CREATE TABLE IF NOT EXISTS users
                        (identifier TEXT PRIMARY KEY ASC, email TEXT, name TEXT, loyalty_program_user_id TEXT,
                        fitbit_access_token TEXT, fitbit_refresh_token TEXT, fitbit_token_expiry TEXT,
                        fitbit_id TEXT)''')
    cursor.execute(''' CREATE TABLE IF NOT EXISTS challenges
                        (identifier TEXT PRIMARY KEY ASC, name TEXT, steps_to_unlock INTEGER, loyalty_program_merchant_user_id TEXT,
                        expiry_timestamp TEXT, reward_points INTEGER)''')
    cursor.execute(''' CREATE TABLE IF NOT EXISTS user_challenge
                        (user_identifier INTEGER, challenge_identifier INTEGER,
                        user_total_step_count_on_start INTEGER, user_total_step_count_on_expiry INTEGER,
                        status TEXT, PRIMARY KEY (user_identifier, challenge_identifier),
                        FOREIGN KEY(user_identifier) REFERENCES users(identifier),
                        FOREIGN KEY(challenge_identifier) REFERENCES challenges(identifier))''')
    _seed_challenges(cursor)


def _seed_challenges(cursor):
    challenges = [
        ('1', 'Get 100 GR Points For 10 steps', 10, 'merchant_GR_123', '2016-10-01 12:12:12.777', 100),
        ('2', 'Get 200 GR Points For 20 steps', 20, 'merchant_GR_123', '2016-10-01 12:12:12.777', 200),
        ('3', 'Get 300 GR Points For 30 steps', 30, 'merchant_GR_123', '2016-10-01 12:12:12.777', 300),
        ('4', 'Get 400 GR Points For 40 steps', 40, 'merchant_GR_123', '2016-10-01 12:12:12.777', 400),
        ('5', 'Get 500 GR Points For 50 steps', 50, 'merchant_GR_123', '2016-10-01 12:12:12.777', 500)
    ]
    cursor.execute('INSERT INTO challenges VALUES(?,?,?,?,?,?)', challenges)


def create_user(name, email, loyalty_program_user_id, access_token, refresh_token, token_expiry, fitbit_id):
    cursor = connection.cursor()
    user_id = str(uuid.uuid1())
    cursor.execute(''' INSERT INTO users
                      (identifier, email, name, loyalty_program_user_id,
                      fitbit_access_token, fitbit_refresh_token, fitbit_token_expiry,
                      fitbit_id)
                      VALUES (?,?,?,?,?,?,?,?);''', (user_id, email, name,
                                                     loyalty_program_user_id, access_token,
                                                     refresh_token, token_expiry, fitbit_id))
    return user_id
