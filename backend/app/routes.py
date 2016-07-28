import httplib
import json

from flask import Flask, render_template, request, Response

app = Flask(__name__)


# POST /user?fitbit_token=<aaa>
@app.route('/user', methods=['POST'])
def fitbit_user():
    fitbit_token = request.args.get('fitbit_token', '')
    user = {
        'fitbitToken': fitbit_token,
        'identifier': 123
    }
    return Response(json.dumps(user), status=httplib.CREATED, mimetype='application/json')


@app.route('/user/<userid>/challenges/_<status>', methods=['GET'])
def challenge_status(userid, status):
    challenges = [{
        'challengeName': 'some name',
        'identifier': 123,
        'userIdentifier': userid,
        'status': status
    }]
    return Response(json.dumps(challenges), status=httplib.OK, mimetype='application/json')


if __name__ == '__main__':
    app.run(debug=True)
