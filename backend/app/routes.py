import httplib
import json
import sqlite3
import logging
import sys

from flask import Flask, request, Response
from flask_cors import CORS

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
logger.addHandler(handler)

app = Flask(__name__)
CORS(app)


@app.route('/user', methods=['POST'])
def fitbit_user():
    """
        POST /user?fitbit_token=<aaa>
    """
    fitbit_token = request.args.get('fitbit_token', '')
    logger.debug('Creating user with token %s', fitbit_token)
    user = {
        'fitbitToken': fitbit_token,
        'userId': 123
    }

    # Get users fitbit email and current step count.

    # Save the user model in the database

    return Response(json.dumps(user), status=httplib.CREATED, mimetype='application/json')


@app.route('/user/<user_id>/challenges/_<status>', methods=['GET'])
def challenge_status(user_id, status):
    """
    GET /user/<user_id>/challenges/_new
    GET /user/<user_id>/challenges/_accepted
    :param user_id:
    :param status:
    :return:
    """
    challenges = [{
        'challengeName': 'some name',
        'challengeId': 123,
        'userId': user_id,
        'status': status
    }]
    return Response(json.dumps(challenges), status=httplib.OK, mimetype='application/json')


@app.route('/challenges/<challenge_id>/user/<user_id>', methods=['POST'])
def user_challenge(challenge_id, user_id):
    """
        POST /challenges/<challenge_id>/user/<user_id>
    :param challenge_id:
    :param user_id:
    :return:
    """
    user = {
        'challengeId': challenge_id,
        'userId': user_id
    }
    return Response(json.dumps(user), status=httplib.CREATED, mimetype='application/json')


@app.route('/challenges/_expire', methods=['POST'])
def expire_user_challenges():
    """
        POST /challenges/_expire
        When invoked, this endpoint will go through all the expired challenges and
        update the status of all users who have accepted this challenge.
    :param challenge_id:
    :param user_id:
    :return:
    """
    user = [{
        'challengeId': 777,
        'userId': 333
    }]
    return Response(json.dumps(user), status=httplib.CREATED, mimetype='application/json')


def initialize_db():
    logger.debug('Initializing database ...')
    connection = sqlite3.connect('pointsboost.db')
    cursor = connection.cursor()
    cursor.execute(''' CREATE TABLE IF NOT EXISTS users
                        (identifier INTEGER PRIMARY KEY ASC, email TEXT, name TEXT, loyalty_program_user_id TEXT,
                        fitbit_access_token TEXT, fitbit_refresh_token TEXT, fitbit_token_expiry TEXT,
                        fitbit_id TEXT)''')
    cursor.execute(''' CREATE TABLE IF NOT EXISTS challenge
                        (identifier INTEGER PRIMARY KEY ASC, name TEXT, steps_to_unlock INTEGER, loyalty_program_merchant_user_id TEXT,
                        expiry_timestamp TEXT, reward_points INTEGER)''')
    cursor.execute(''' CREATE TABLE IF NOT EXISTS user_challenge
                        (user_identifier INTEGER, challenge_identifier INTEGER,
                        user_total_step_count_on_start INTEGER, user_total_step_count_on_expiry INTEGER,
                        status TEXT, PRIMARY KEY (user_identifier, challenge_identifier),
                        FOREIGN KEY(user_identifier) REFERENCES users(identifier),
                        FOREIGN KEY(challenge_identifier) REFERENCES challenge(identifier))''')


if __name__ == '__main__':
    initialize_db()
    app.run(debug=True)
