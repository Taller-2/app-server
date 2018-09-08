from server.libs.mongo import mongo

from flask import jsonify


def get(args, col):
    data = mongo.db[col].find_one(args)
    return data


def post(data, col):
    result = mongo.db[col].insert_one(data)
    if not result.acknowledged:
        dicc = {'ok': False, 'message': 'Bad request parameters!'}
        return jsonify(dicc), 400
    return jsonify({'ok': True, 'message': 'User created successfully!'}), 200


def delete(data, col):
    db_response = mongo.db[col].delete_one({'id': data['id']})
    return db_response


def patch(data, col):
    if not data.get('query', {}) != {}:
        return False
    mongo.db[col].update_one(data['query'], {'$set': data.get('payload', {})})
    return True
