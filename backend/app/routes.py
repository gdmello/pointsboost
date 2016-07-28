import httplib
import json

from flask import Flask, render_template, request, Response

app = Flask(__name__)


@app.route('/user', methods=['POST'])
def fitbit_user():
    """
        POST /user?fitbit_token=<aaa>
    """
    fitbit_token = request.args.get('fitbit_token', '')
    user = {
        'fitbitToken': fitbit_token,
        'userId': 123
    }
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


@app.route('challenges/<challenge_id>/user/<user_id>', methods=['POST'])
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


if __name__ == '__main__':
    app.run(debug=True)
