from flask import request, jsonify, Blueprint

from server.libs.mongo import mongo

MONGO_TEST = Blueprint('mongo_test', __name__, url_prefix='/user')


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


@MONGO_TEST.route('/', methods=['GET', 'POST', 'DELETE', 'PATCH'])
def user():
    if request.method == 'GET':
        return user_get()
    data = request.get_json()
    if request.method == 'POST':
        return user_post(data)
    if request.method == 'DELETE':
        return user_delete(data)
    return user_patch(data)
