import httplib
import json

from flask import Flask, render_template, request, Response

app = Flask(__name__)


@app.route('/user', methods=['POST', 'GET'])
def fitbit_user():
    """
        POST /user?access_token=<aaa>

    """
    access_token = request.args.get('access_token', '')
    user_id = request.args.get('user_id', '')
    lifetimeSteps = get_steps(user_id, access_token)

    user = {
        'access_token': access_token,
        'userId': user_id,
        'lifetimeSteps': lifetimeSteps
    }

    # Get users fitbit email and points balance.

    #eg: https://api.fitbit.com/1/user/4KRQ6L/activities.json

    # Save the user model in the database

    return Response(json.dumps(user), status=httplib.CREATED, mimetype='application/json')

def get_steps(user_id, access_token):
    """
        GET https://api.fitbit.com/1/user/user_id/activities.json
    """
    steps = request.args.get('tracker/steps', '')
    return steps

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


if __name__ == '__main__':
    app.run(debug=True)
