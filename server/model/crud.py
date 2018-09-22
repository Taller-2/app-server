from bson.objectid import ObjectId
from flask import jsonify

from server.libs.mongo import mongo


def get(args, col):
    data = mongo.db[col].find(args)
    return list(data)


def post(data, col, attributes=None):
    if attributes:
        try:
            data = {attribute: data[attribute] for attribute in attributes}
        except KeyError as error:
            return jsonify({
                'ok': False,
                'message': 'Missing attribute: ' + error.args[0]
            }), 400
    result = mongo.db[col].insert_one(data)
    if not result.acknowledged:
        return jsonify({'ok': False, 'message': 'Bad parameters'}), 400
    return jsonify({'ok': True, 'message': 'Created'}), 200


def delete(data, col):
    db_response = mongo.db[col].delete_one({'_id': ObjectId(data['id'])})
    return db_response


def patch(data, col):
    if not data.get('query', {}) != {}:
        return False
    mongo.db[col].update_one(data['query'], {'$set': data.get('payload', {})})
    return True
