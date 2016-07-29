import httplib
import json
import logging
import sys

from flask import Flask, request, Response
from flask_cors import CORS

import database

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

    # TODO: Prerna: Get users fitbit email and current step count and set values in database.create_user

    # Save the user model in the database
    user_id = database.create_user(name='Ezra Lampstand', email='ezra.l@gmail.com', loyalty_program_user_id='GlobalRewards123',
                         access_token='some_access_token', refresh_token='some refresh token',
                         token_expiry='2016-10-01 12:12:12.777', fitbit_id='fitbit_123')

    user = {
        'fitbitToken': fitbit_token,
        'userId': user_id,
        'name': 'Ezra Lampstand',
        'points_balance': 42
    }
    return Response(json.dumps(user), status=httplib.CREATED, mimetype='application/json')


@app.route('/users/<user_id>/challenges/_<status>', methods=['GET'])
def challenge_status(user_id, status):
    """
    GET /user/<user_id>/challenges/_new
    GET /user/<user_id>/challenges/_accepted
    :param user_id:
    :param status:
    :return:
    """
    challenges = database.user_challenges(user_id, status)
    return Response(json.dumps(challenges), status=httplib.OK, mimetype='application/json')


@app.route('/users/<user_id>/challenges/<challenge_id>', methods=['POST'])
def user_challenge(challenge_id, user_id):
    """
        POST /challenges/<challenge_id>/user/<user_id>
    :param challenge_id:
    :param user_id:
    :return:
    """
    # TODO: Prerna; Get users total step count from fitbit and set it to 'user_fitbit_total_steps' below

    database.user_challenge(user_id, challenge_id, user_fitbit_total_steps=1)

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


if __name__ == '__main__':
    logger.debug('Initializing database ...')
    database.initialize()
    database.seed_challenges()
    app.run(debug=True)
