import datetime
import json

from bson.objectid import ObjectId
from flask import Flask, request, jsonify, render_template
from flask_pymongo import PyMongo


class JSONEncoder(json.JSONEncoder):
    # extend json encoder for compatibility with mongoDB
    def default(self, o):  # pylint: disable=E0202
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, datetime.datetime):
            return str(o)
        return json.JSONEncoder.default(self, o)


app = Flask(__name__)  # pylint: disable=C0103
mongo = PyMongo(app)  # pylint: disable=C0103
app.config['MONGO_URI'] = 'mongodb://localhost:27017/myDatabase'
app.json_encoder = JSONEncoder


@app.route('/')
def index():
    return render_template('index.html')


# mongoDB test
def user_get():
    data = mongo.db.users.find_one(request.args)
    return jsonify(data), 200


def user_post(data):
    if not all(key in data.keys() for key in ['name', 'email']):
        return jsonify(
            {'ok': False, 'message': 'Bad request parameters!'}
        ), 400
    mongo.db.users.insert_one(data)
    return jsonify({'ok': True, 'message': 'User created successfully!'}), 200


def user_delete(data):
    if 'email' not in data:
        return jsonify(
            {'ok': False, 'message': 'Bad request parameters!'}
        ), 400
    db_response = mongo.db.users.delete_one({'email': data['email']})
    if db_response.deleted_count == 1:
        response = {'ok': True, 'message': 'record deleted'}
    else:
        response = {'ok': True, 'message': 'no record found'}
    return jsonify(response), 200


def user_patch(data):
    if not data.get('query', {}) != {}:
        return jsonify(
            {'ok': False, 'message': 'Bad request parameters!'}
        ), 400
    mongo.db.users.update_one(
        data['query'],
        {'$set': data.get('payload', {})}
    )
    return jsonify({'ok': True, 'message': 'record updated'}), 200


@app.route('/user', methods=['GET', 'POST', 'DELETE', 'PATCH'])
def user():
    if request.method == 'GET':
        return user_get()
    data = request.get_json()
    if request.method == 'POST':
        return user_post(data)
    if request.method == 'DELETE':
        return user_delete(data)
    return user_patch(data)  # request.method == 'PATCH'
