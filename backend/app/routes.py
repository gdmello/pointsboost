import httplib
import json
import sqlite3
import logging
import sys

from flask import Flask, request, Response


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
logger.addHandler(handler)

app = Flask(__name__)


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
                        (identifier integer PRIMARY KEY ASC, email text, name text, loyalty_program_user_id text,
                        fitbit_access_token text, fitbit_refresh_token text, fitbit_token_expiry text,
                        fitbit_id text)''')
    cursor.execute(''' CREATE TABLE IF NOT EXISTS challenge
                        (identifier integer PRIMARY KEY ASC, name text, steps_to_unlock integer, loyalty_program_merchant_user_id text,
                        expiry_timestamp text, reward_points integer)''')
    cursor.execute(''' CREATE TABLE IF NOT EXISTS user_challenge
                        (user_identifier integer, challenge_identifier integer,
                        user_total_step_count_on_start integer, user_total_step_count_on_expiry integer,
                        status text, PRIMARY KEY (user_identifier, challenge_identifier),
                        FOREIGN KEY(user_identifier) REFERENCES users(identifier),
                        FOREIGN KEY(challenge_identifier) REFERENCES challenge(identifier))''')


if __name__ == '__main__':
    initialize_db()
    app.run(debug=True)
