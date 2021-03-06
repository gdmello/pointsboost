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
    #get lifetimfe stats https://api.fitbit.com/1/user/4KRQ6L/activities.json
    # Get users fitbit email and points balance.

    # eg: https://api.fitbit.com/1/user/4KRQ6L/activities.json


    fitbit_id = request.args.get('user_id', '')
    user = database.get_user_by_fitbit(fitbit_id)

    if user is None:
        if len(access_token) > 0:
            fitbit_api = fitbit.Fitbit('227QRF', 'aacdb90aaaa175c50e0556e1a50f35ab',access_token=access_token)
            name = fitbit_api.user_profile_get(fitbit_id)['user']['fullName']
            database.create_user(name=name, email='ezra.l@gmail.com', loyalty_program_user_id='GlobalRewards123',
                                        access_token=access_token, refresh_token='some refresh token',
                                        token_expiry='2016-10-01 12:12:12.777', fitbit_id=fitbit_id, points=20146)
        else:
            raise StandardError("no user found, or access token sent")
        user = database.get_user_by_fitbit(fitbit_id)


    if len(access_token) > 0:
        database.update_user_token(user.get('userIdentifier'), access_token)


    #points_balance = lcp_query.get_balance(user_id)
    #points_balance = 549
    userJSON = {
        'access_token': access_token,
        'userId': user.get('userIdentifier'),
        'points_balance': user.get('points'),
        'name': user.get('name'),
        'fitbitId':user.get('fitbit_id')
    }
    return Response(json.dumps(userJSON), status=httplib.CREATED, mimetype='application/json')


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
    user = database.get_user(user_id)
    print(user)
    access_token = user.get('fitbit_access_token')
    totalPoints = user.get('points')
    fitbit_api = fitbit.Fitbit('4KRQ6L', 'aacdb90aaaa175c50e0556e1a50f35ab',access_token=access_token)
    activity_stats = fitbit_api.activity_stats(user_id=user.get('fitbit_id'))
    resp = {
        'steps': activity_stats['lifetime']['tracker']['steps'],
        'points': totalPoints
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
    :param challenge_id:
    :param user_id:
    :return:
    """
    # TODO: Prerna; Get users total step count from fitbit and set it to 'user_fitbit_total_steps' below
    user = database.get_user(user_id)
    action = fitbit_id = request.args.get('action', '')
    if action == 'reject':
        challenge = database.destroy_user_challenge(challenge_id, user_id)
        user = {}
    else:
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
    for user_challenge in expired_user_challenges:
        user_id = user_challenge.get('userIdentifier')
        user = database.get_user(user_id)
        fitbit_api = fitbit.Fitbit('227QRF', 'aacdb90aaaa175c50e0556e1a50f35ab',
                                   access_token=user.get('fitbit_access_token'))
        activity_stats = fitbit_api.activity_stats(user_id=user.get('fitbit_id'))
        steps = activity_stats['lifetime']['tracker']['steps']
        challenge_id = user_challenge.get('challengeIdentifier')
        uc = database.get_user_challenge(user_id, challenge_id)
        challenge = database.get_challenge(challenge_id)
        if (steps - uc.get('user_total_step_count_on_start')) >= challenge.get('steps_to_unlock'):
            database.user_challenge_complete(user_id, challenge_id, challenge.get('reward_points'))



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
