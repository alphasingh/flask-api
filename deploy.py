# Using flask to make an api 
# import necessary libraries and functions 
from flask import Flask, jsonify, request
from flask_restplus import Api, Resource, fields
from werkzeug.exceptions import BadRequest

# creating a Flask app
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
api = Api(app)

apiStatus = {
    'status': 'up',
    'docs': 'https://appscoop-mock-api-test0.herokuapp.com',
    'contribute': 'https://github.com/alphasingh/flask-api',
    'author': 'Abhay Raj Singh',
    'created': '27 March 2020',
    'updated': '9 June 2021'
}


@app.route('/status', methods=['POST', 'GET'])
def getApiStatus():
    return jsonify(apiStatus), 200


# @app.before_request
def authorizeRequest():
    bearer = request.headers.get('Authorization')
    e = BadRequest('No Authorization provided in headers. Attach a valid bearer token.')
    e.data = {'Access': 'Denied', 'CODE': 'Unauthorized'}
    if bearer is None or 'Bearer' not in bearer:
        raise e


@app.after_request
def attach_custom_headers_on_response(response):
    response.headers["Updated"] = "9 June 2021"
    response.headers["Contribute"] = "https://github.com/alphasingh/flask-api"
    return response


'''
Driver related schedules
'''
ns = api.namespace('drivers-schedules', description='Operations related to driver schedules')
driverScheduleModel = api.model('DriverSchedule', {
    'id': fields.Integer(description='The unique identifier of the schedule'),
    'driverId': fields.Integer(required=True, description='The unique identifier of the driver'),
    'zoneId': fields.Integer(required=True, description='The unique identifier of the zone in which driver will work'),
    'startTime': fields.DateTime(required=True, description='The start time of this driver schedule'),
    'endTime': fields.DateTime(required=True, description='The end time of this driver schedule'),
    'createdAt': fields.DateTime,
    'updatedAt': fields.DateTime
})
driverSchedules = [
    {'id': 1, 'driverId': 5, 'zoneId': 4, 'startTime': '2020-03-31T02:26:10Z', 'endTime': '2020-03-31T12:26:10Z',
     'createdAt': '2020-03-25T02:26:10Z', 'updatedAt': '2020-03-25T02:26:10Z'},
    {'id': 2, 'driverId': 4, 'zoneId': 4, 'startTime': '2020-03-31T02:26:10Z', 'endTime': '2020-03-31T12:26:10Z',
     'createdAt': '2020-03-25T02:26:10Z', 'updatedAt': '2020-03-25T02:26:10Z'},
    {'id': 3, 'driverId': 5, 'zoneId': 5, 'startTime': '2020-03-32T02:26:10Z', 'endTime': '2020-03-31T12:26:10Z',
     'createdAt': '2020-03-25T02:26:10Z', 'updatedAt': '2020-03-25T02:26:10Z'}
]
updateKeys = {'driverId', 'zoneId', 'startTime', 'endTime'}


@ns.route('/')
class DriverSchedule(Resource):
    @ns.response(201, 'Driver schedule successfully created.')
    @ns.expect(driverScheduleModel)
    @ns.marshal_with(driverScheduleModel, code=201)
    def post(self):
        return jsonify(driverSchedules[0]), 201

    @ns.response(400, 'Driver schedule does not exist.')
    @ns.response(200, 'Driver exists with dummy values.')
    def get(self):
        return {'name': 'Driver'}, 200


# driver function
if __name__ == '__main__':
    app.run(debug=True)
