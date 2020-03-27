# Using flask to make an api 
# import necessary libraries and functions 
from flask import Flask, jsonify, request

# creating a Flask app 
app = Flask(__name__)

# on the terminal type: curl http://127.0.0.1:5000/ 
# returns hello world when we use GET. 
# returns the data that we send when we use POST. 
@app.route('/', methods = ['GET', 'POST'])
def home():
        status = "up"
        return jsonify({'status': status})


# A simple function to calculate the square of a number 
# the number to be squared is sent in the URL when we use GET 
# on the terminal type: curl http://127.0.0.1:5000 / home / 10 
# this returns 100 (square of 10) 
@app.route('/square/<int:num>', methods = ['GET'])
def disp(num):
        return jsonify({'data': num**2}), 201


"""
Function returns the dummy matrix in response
"""
@app.route('/matrix', methods = ['GET'])
def matrix():
        status = "up"
        return jsonify({'status': status})


# login
@app.route(...)
def login():
        username = request.args.get('username')
        password = request.args.get('password')
        status = false
        if username == 'user' and password == 'pass':
              status = true
        return jsonify({'authorized': status})


# driver function 
if __name__ == '__main__':
        app.run(debug = True)
