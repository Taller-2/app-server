from flask import Flask, request, jsonify, render_template
from flask_pymongo import PyMongo
import json
import datetime
from bson.objectid import ObjectId

class JSONEncoder(json.JSONEncoder):
    # extend json encoder for compatibility with mongoDB
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, datetime.datetime):
            return str(o)
        return json.JSONEncoder.default(self, o)

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/myDatabase'
app.json_encoder = JSONEncoder
mongo = PyMongo(app)

@app.route('/')
def index():
    return render_template('index.html')

# mongoDB test
@app.route('/user', methods=['GET', 'POST', 'DELETE', 'PATCH'])
def user():
    if request.method == 'GET':
        data = mongo.db.users.find_one(request.args)
        return jsonify(data), 200

    data = request.get_json()
    if request.method == 'POST':
        if not all(key in data.keys() for key in ['name', 'email']):
            return jsonify({'ok': False, 'message': 'Bad request parameters!'}), 400
        mongo.db.users.insert_one(data)
        return jsonify({'ok': True, 'message': 'User created successfully!'}), 200

    if request.method == 'DELETE':
        if 'email' not in data:
            return jsonify({'ok': False, 'message': 'Bad request parameters!'}), 400
        db_response = mongo.db.users.delete_one({'email': data['email']})
        if db_response.deleted_count == 1:
            response = {'ok': True, 'message': 'record deleted'}
        else:
            response = {'ok': True, 'message': 'no record found'}
        return jsonify(response), 200

    if request.method == 'PATCH':
        if not data.get('query', {}) != {}:
            return jsonify({'ok': False, 'message': 'Bad request parameters!'}), 400
        mongo.db.users.update_one(
            data['query'],
            {'$set': data.get('payload', {})}
        )
        return jsonify({'ok': True, 'message': 'record updated'}), 200
