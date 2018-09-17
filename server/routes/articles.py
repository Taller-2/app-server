from bson.json_util import dumps
from flask import request, Blueprint, Response, jsonify

from server.libs.mongo import mongo
from server.model import crud

ARTICLES_BP = Blueprint('articles', __name__, url_prefix='/article')


@ARTICLES_BP.route('/<_id>/', methods=['DELETE'])
def delete_article(_id):
    deleted = crud.delete({'id': _id}, 'articles').deleted_count == 1
    if not deleted:
        return jsonify({'ok': False}), 500
    return jsonify({'ok': True, 'message': 'Deleted'}), 200


@ARTICLES_BP.route('/', methods=['GET', 'POST'])
def article():
    if request.method == 'GET':
        return Response(
            response=dumps(mongo.db['articles'].find(request.args)),
            status=200,
            mimetype='application/json'
        )
    return crud.post(
        request.get_json(),
        'articles',
        ('name', 'description', 'available_units', 'price')
    )
