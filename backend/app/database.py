import sqlite3
import uuid
import logging
import sys

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
logger.addHandler(handler)


def _connection():
    return sqlite3.connect('pointsboost.db', check_same_thread=False, timeout=10)


def initialize():
    connection = _connection()
    cursor = connection.cursor()
    cursor.execute(''' CREATE TABLE IF NOT EXISTS users
                        (identifier TEXT PRIMARY KEY ASC, email TEXT, name TEXT, loyalty_program_user_id TEXT,
                        fitbit_access_token TEXT, fitbit_refresh_token TEXT, fitbit_token_expiry TEXT,
                        fitbit_id TEXT)''')
    cursor.execute(''' CREATE TABLE IF NOT EXISTS challenges
                        (identifier TEXT PRIMARY KEY, name TEXT, steps_to_unlock INTEGER, loyalty_program_merchant_user_id TEXT,
                        expiry_timestamp TEXT, reward_points INTEGER)''')
    cursor.execute(''' CREATE TABLE IF NOT EXISTS user_challenge
                        (user_identifier INTEGER, challenge_identifier INTEGER,
                        user_total_step_count_on_start INTEGER, user_total_step_count_on_expiry INTEGER,
                        status TEXT, PRIMARY KEY (user_identifier, challenge_identifier),
                        FOREIGN KEY(user_identifier) REFERENCES users(identifier),
                        FOREIGN KEY(challenge_identifier) REFERENCES challenges(identifier))''')
    connection.commit


def seed_challenges():
    logger.debug('seeding challenges ...')
    connection = _connection()
    cursor = connection.cursor()
    challenges = [
        ('1', 'Get 100 GR Points For 10 steps', 10, 'merchant_GR_123', '2016-10-01 12:12:12.777', 100),
        ('2', 'Get 200 GR Points For 20 steps', 20, 'merchant_GR_123', '2016-10-01 12:12:12.777', 200),
        ('3', 'Get 300 GR Points For 30 steps', 30, 'merchant_GR_123', '2016-10-01 12:12:12.777', 300),
        ('4', 'Get 400 GR Points For 40 steps', 40, 'merchant_GR_123', '2016-10-01 12:12:12.777', 400),
        ('5', 'Get 500 GR Points For 50 steps', 50, 'merchant_GR_123', '2016-10-01 12:12:12.777', 500),
    ]

    cursor.executemany('''INSERT OR IGNORE INTO challenges(identifier, name, steps_to_unlock, loyalty_program_merchant_user_id,
                        expiry_timestamp, reward_points)
                          VALUES (?,?,?,?,?,?)
                      ''', challenges)
    connection.commit()


def create_user(name, email, loyalty_program_user_id, access_token, refresh_token, token_expiry, fitbit_id):
    connection = _connection()
    cursor = connection.cursor()
    user_id = str(uuid.uuid1())
    cursor.execute(''' INSERT INTO users
                      (identifier, email, name, loyalty_program_user_id,
                      fitbit_access_token, fitbit_refresh_token, fitbit_token_expiry,
                      fitbit_id)
                      VALUES (?,?,?,?,?,?,?,?);''', (user_id, email, name,
                                                     loyalty_program_user_id, access_token,
                                                     refresh_token, token_expiry, fitbit_id))
    connection.commit()
    return user_id


def user_challenges(user_id, status='new'):
    cursor = _connection().cursor()
    if status == 'new':
        cursor.execute('''
                        SELECT * FROM challenges WHERE identifier NOT IN (
                          SELECT challenge_identifier FROM user_challenge WHERE
                            user_identifier=?
                        )
                      ''', (user_id,))
    else:
        cursor.execute('''
                        SELECT * FROM challenges WHERE identifier IN (
                          SELECT challenge_identifier FROM user_challenge WHERE
                            user_identifier=?
                        )
                      ''', (user_id,))
    challenges = []
    for row in cursor.fetchall():
        challenges.append(dict(
            challengeIdentifier=row[0],
            name=row[1],
            stepsToUnlock=row[2],
            expiryTimestamp=row[4],
            rewardPoints=row[5]
        ))
    return challenges


def user_challenge(user_id, challenge_id, user_fitbit_total_steps):
    connection = _connection()
    cursor = connection.cursor()
    cursor.execute(''' INSERT INTO user_challenge
                        (user_identifier, challenge_identifier, user_total_step_count_on_start, status)
                          VALUES (?,?,?,?);''', (user_id, challenge_id, user_fitbit_total_steps, 'in-progress'))
    connection.commit()
