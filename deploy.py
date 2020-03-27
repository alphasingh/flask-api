# Using flask to make an api 
# import necessary libraries and functions 
from flask import Flask, jsonify, request
from flask_restplus import Api, Resource, fields


# creating a Flask app 
app = Flask(__name__)
api = Api(app, version='1.0', title='Todo API',
    description='A simple TODO API extracted from the original flask-restful example'
)
ns = api.namespace('squares', description='square operations')

# on the terminal type: curl http://127.0.0.1:5000/ 
# returns hello world when we use GET. 
# returns the data that we send when we use POST. 
@api.doc(responses={404: 'Todo not found'}, params={'todo_id': 'The Todo ID'})
@app.route('/', methods = ['GET', 'POST'])
def home():
        status = "up"
        return jsonify({'status': status})


# A simple function to calculate the square of a number 
# the number to be squared is sent in the URL when we use GET 
# on the terminal type: curl http://127.0.0.1:5000 / home / 10 
# this returns 100 (square of 10) 
@ns.route('/square/<int:num>', methods = ['GET'])
def disp(num):
        return jsonify({'data': num**2}), 201


"""
Function returns the dummy matrix in response
"""
@api.route('/matrix', methods = ['GET'])
def matrix():
        status = "up"
        return jsonify({'status': status})


@app.route('/matrix', methods = ['POST'])
def createCompatibility():
        password = request.args.get('password')
        page = request.args.get('page', default = 1, type = int)
        return jsonify({'pass': password, 'pageSizeRequested': page})


@app.route('/api/users', methods = ['POST'])
def createNewUser():
    username = request.json.get('username')
    password = request.json.get('password')
    if username is None or password is None:
        abort(400) # missing arguments
    return jsonify({ 'username': username, 'password': username  }), 201, {'Location': url_for('get_user', id = user.id, _external = True)}


# driver function 
if __name__ == '__main__':
        app.run(debug = True)
