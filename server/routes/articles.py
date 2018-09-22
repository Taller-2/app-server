from bson.json_util import dumps
from flask import request, Blueprint, Response, jsonify

from server.decorators.login_required import login_required
from server.libs.mongo import mongo
from server.model import crud
from server.utils import response

ARTICLES_BP = Blueprint('articles', __name__, url_prefix='/article')


@ARTICLES_BP.route('/<_id>/', methods=['DELETE'])
def delete_article(_id):
    deleted = crud.delete({'id': _id}, 'articles').deleted_count == 1
    if not deleted:
        return response(message=f"Error deleting article {_id}", ok=False), 500
    return response(message=f"Successfully deleted article {_id}", ok=True), 200


@ARTICLES_BP.route('/', methods=['GET'])
def get_article():
    return Response(
        response=dumps(mongo.db['articles'].find(request.args)),
        status=200,
        mimetype='application/json'
    )


@login_required
@ARTICLES_BP.route('/', methods=['POST'])
def post_article():
    return crud.post(
        request.get_json(),
        'articles',
        ('name', 'description', 'available_units', 'price')
    )
