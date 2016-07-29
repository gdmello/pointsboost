import httplib
import json
import logging
import sys
from flask import Flask, request, Response
from flask_cors import CORS
import fitbit

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
        POST /user?access_token=<aaa>&user_id=<fitbit_user_id>

    """
    access_token = request.args.get('access_token', '')
    logger.debug('Creating user with token %s', access_token)
    fitbit_id = request.args.get('user_id', '')
    fitbit_api = fitbit.Fitbit('227QRF', 'aacdb90aaaa175c50e0556e1a50f35ab',access_token=access_token)
    name = fitbit_api.user_profile_get(fitbit_id)['user']['fullName']
    #get lifetimfe stats https://api.fitbit.com/1/user/4KRQ6L/activities.json
    # Get users fitbit email and points balance.

    # eg: https://api.fitbit.com/1/user/4KRQ6L/activities.json

    # Save the user model in the database
    user = database.create_user(name=name, email='ezra.l@gmail.com', loyalty_program_user_id='GlobalRewards123',
                         access_token=access_token, refresh_token='some refresh token',
                         token_expiry='2016-10-01 12:12:12.777', fitbit_id=fitbit_id)

    #points_balance = lcp_query.get_balance(user_id)
    points_balance = 549
    user = {
        'access_token': access_token,
        'userId': user
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
    access_token = database.get_user(user_id).access_token
    fitbit_api = fitbit.Fitbit('227QRF', 'aacdb90aaaa175c50e0556e1a50f35ab',access_token=access_token)
    activity_stats = fitbit_api.activity_stats(user_id=user_id)
    resp = {
        'steps': activity_stats['lifetime']['tracker']['steps']
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
    user = database.get_user(user_id)
    access_token = user.get('fitbit_access_token')
    fitbit_api = fitbit.Fitbit('227QRF', 'aacdb90aaaa175c50e0556e1a50f35ab',access_token=access_token)
    activity_stats = fitbit_api.activity_stats(user_id=user.get('fitbit_id'))
    steps = activity_stats['lifetime']['tracker']['steps']
    database.user_challenge(user_id, challenge_id, user_fitbit_total_steps=steps)

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
    import ipdb
    ipdb.set_trace()
    expired_user_challenges = database.get_expired_challenges()
    for challenge in expired_user_challenges:
        print "hi"

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
