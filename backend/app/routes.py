import httplib
import json
import logging
import sys
from flask import Flask, render_template, request, Response
from flask_cors import CORS

import database

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
logger.addHandler(handler)

app = Flask(__name__)
CORS(app)


@app.route('/user', methods=['POST', 'GET'])
def fitbit_user():
    """
        POST /user?access_token=<aaa>

    """
    access_token = request.args.get('access_token', '')
    logger.debug('Creating user with token %s', access_token)
    fitbit_id = request.args.get('user_id', '')
    name = request.args.get('displayName', '')
    # Get users fitbit email and points balance.

    # eg: https://api.fitbit.com/1/user/4KRQ6L/activities.json

    # Save the user model in the database
    user_id = database.create_user(name=name, email='ezra.l@gmail.com', loyalty_program_user_id='GlobalRewards123',
                                   access_token=access_token, refresh_token='some refresh token',
                                   token_expiry='2016-10-01 12:12:12.777', fitbit_id=fitbit_id)

    #points_balance = lcp_query.get_balance(user_id)
    points_balance = 549
    user = {
        'access_token': access_token,
        'userId': user_id,
        'name': name,
        'points_balance': points_balance 
    }
    return Response(json.dumps(user), status=httplib.CREATED, mimetype='application/json')


def get_steps(user_id, access_token):
    """
        GET https://api.fitbit.com/1/user/user_id/activities.json
    """
    steps = request.args.get('tracker/steps', '')
    return steps


@app.route('/user/<user_id>/activity', methods=['GET'])
def user_activity(user_id):
    """
    GET /user/<user_id>/activity
    :param user_id:
    :param status:
    :return:
    """
    resp = {
        'steps': 2350,
        'calories': 259
    }
    return Response(json.dumps(resp), status=httplib.OK, mimetype='application/json')


@app.route('/user/<user_id>/challenges/_<status>', methods=['GET'])
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
