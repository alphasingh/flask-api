# Using flask to make an api 
# import necessary libraries and functions 
from flask import Flask, jsonify, request
from flask_restplus import Api, Resource, fields
from werkzeug.exceptions import BadRequest


# creating a Flask app 
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
api = Api(app)


#################################################################################################################
#       API STATUS
#################################################################################################################
nsApiStatus = api.namespace('status', description='Restful API status')
apiStatus = {
                "status":"up",
                "docs":"https://appscoop-mock-api-test0.herokuapp.com",
                "contribute":"https://github.com/alphasingh/flask-api",
                "author":{
                        "name":"Abhay Raj Singh",
                        "contact":"abhayraja4@gmail.com",
                        "since":"27 March 2020"
                }
}
@nsApiStatus.route('/')
class ApiStatus(Resource):
        @nsApiStatus.response(200, 'Latest API information successfully fetched.')
        def post(self):
                return (jsonify(apiStatus), 200)


#################################################################################################################
#       SQUARE OF A NUMBER
#################################################################################################################
nsSquareOfNumber = api.namespace('square', description='Calculate square of a number')
@nsSquareOfNumber.route('/')
class SquareOfNumber(Resource):
        @nsSquareOfNumber.response(200, 'Successfully returned square of the given number.')
        @nsSquareOfNumber.route('/<int:number>')
        def get(self):
                return (jsonify({"number":number, "square": number**2}), 200)


"""
Function returns the dummy matrix in response
"""
@app.route('/product/compatible', methods = ['GET'])
def getCompatibility():
        authorizeRequest()
        return jsonify([
            {'id': 1, 'name': 'Product 1', 'shortDescription': 'SD', 'fullDescription': 'FD', 'compatibleProducts':[14,4], 'categoryId':1, 'media':{'id':1,'key':'s3objectkey1', 'url':'https://swagger.io/'}},
            {'id': 2, 'name': 'Product 2', 'shortDescription': 'SD2', 'fullDescription': 'FD2', 'compatibleProducts':[14], 'categoryId':2, 'media':{'id':12,'key':'s3objectkey2', 'url':'https://swagger.io/'}},
            {'id': 14, 'name': 'Product 3', 'shortDescription': 'SD14', 'fullDescription': 'FD14', 'compatibleProducts':[1,2,4], 'categoryId':1},
            {'id': 4, 'name': 'Product 4', 'shortDescription': 'SD4', 'fullDescription': 'FD5', 'compatibleProducts':[1,14], 'categoryId':1, 'media':{'id':3,'key':'s3objectkey3', 'url':'https://swagger.io/'}},
            {'id': 3, 'name': 'Product 45', 'shortDescription': 'DS', 'fullDescription': 'DF', 'compatibleProducts':[], 'categoryId':2, 'media':{'id':44,'key':'s3objectkey4', 'url':'https://swagger.io/'}}
        ])


@app.route('/product/compatible', methods = ['PUT', 'DELETE'])
def alterCompatibility():
        authorizeRequest()
        u = request.args.get('productId1')
        v = request.args.get('productId2')
        if u is None or v is None:
                abort(400) # missing arguments or auth header
        return ('', 200)


#@app.before_request
def authorizeRequest():
        bearer = request.headers.get('Authorization')
        e = BadRequest('No Authorization provided in headers. Attach a valid bearer token.')
        e.data = {'Access': 'Denied', 'CODE': 'Unauthorized'}
        if bearer is None or 'Bearer' not in bearer:
                raise e


@app.after_request
def apply_caching(response):
        response.headers["X-custom-header"] = "custom baat cheet"
        return response


@app.route('/api/users', methods = ['POST'])
def createNewUser():
    username = request.json.get('username')
    password = request.json.get('password')
    if username is None or password is None:
        abort(400) # missing arguments
    return jsonify({ 'username': username, 'password': username  }), 201, {'Location': url_for('get_user', id = user.id, _external = True)}


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
                { 'id':1, 'driverId':5, 'zoneId':4, 'startTime':'2020-03-31T02:26:10Z', 'endTime':'2020-03-31T12:26:10Z', 'createdAt':'2020-03-25T02:26:10Z', 'updatedAt':'2020-03-25T02:26:10Z'},
                { 'id':2, 'driverId':4, 'zoneId':4, 'startTime':'2020-03-31T02:26:10Z', 'endTime':'2020-03-31T12:26:10Z', 'createdAt':'2020-03-25T02:26:10Z', 'updatedAt':'2020-03-25T02:26:10Z'},
                { 'id':3, 'driverId':5, 'zoneId':5, 'startTime':'2020-03-32T02:26:10Z', 'endTime':'2020-03-31T12:26:10Z', 'createdAt':'2020-03-25T02:26:10Z', 'updatedAt':'2020-03-25T02:26:10Z'}
        ]
updateKeys = {'driverId', 'zoneId', 'startTime', 'endTime'}
@ns.route('/')
class DriverSchedule(Resource):
        @ns.response(201, 'Driver schedule successfully created.')
        @ns.expect(driverScheduleModel)
        @ns.marshal_with(driverScheduleModel, code=201)
        def post(self):
                return (jsonify(driverSchedules[0]), 201)
        @ns.response(400, 'Driver schedule does not exist.')
        def get(self, id):
                return (jsonify(driverSchedules[1]), 200)

@app.route('/drivers/schedules', methods = ['GET'])
def getAllDriversSchedules():
        return (jsonify(driverSchedules), 200)
@app.route('/drivers/schedules', methods = ['POST'])
def createDriverSchedule():
        authorizeRequest()
        body = request.get_json()
        newScheduleKeys = body.keys()
        #driverScheduleModel.validate(newSchedule)
        for requiredKey in updateKeys:
                if requiredKey not in newScheduleKeys:
                        return (jsonify({'error':'Missing required key:'+requiredKey, 'Given':newScheduleKeys}), 400)
        newSchedule = {}
        newSchedule['id']=len(driverSchedules)+1
        for key in newScheduleKeys:
                if key in updateKeys:
                        newSchedule[key]=body[key]
        newSchedule['createdAt']=newSchedule['startTime']
        newSchedule['updatedAt']=newSchedule['startTime']
        driverSchedules.append(newSchedule)
        return (jsonify(newSchedule), 201)
@app.route('/drivers/schedules/<int:id>', methods = ['PATCH'])
def updateDriverSchedule(id):
        authorizeRequest()
        totalNumberOfSchedules = len(driverSchedules)
        if id > totalNumberOfSchedules or id < 0:
                return (jsonify({'error':'No schedule found for id'}), 400)
        updates = request.get_json()
        existingSchedule = driverSchedules[id-1]
        for key in updates.keys():
                if key in updateKeys:
                        existingSchedule[key]=updates[key]
        return (jsonify(existingSchedule), 200)
@app.route('/drivers/schedules/<int:id>', methods = ['DELETE'])
def deleteDriverSchedule(id):
        authorizeRequest()
        return '', 200



# driver function 
if __name__ == '__main__':
        app.run(debug = True)
