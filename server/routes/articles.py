from bson import ObjectId
from flask import request, Blueprint, jsonify

from server.decorators.login_required import login_required
from server.libs.mongo import validate_object_id
from server.model import crud
from server.model.user import get_user
from server.utils import response

ARTICLES_BP = Blueprint('articles', __name__, url_prefix='/article')


@ARTICLES_BP.route('/<_id>/', methods=['DELETE'])
@login_required
def delete_article(_id):
    if not validate_object_id(_id):
        return response(message=f'{_id} is not a valid Article ID. '
                                f'It must be a 24 byte hexadecimal string',
                        ok=False), 400

    article = crud.get({'_id': ObjectId(_id)}, 'articles')

    if not article:
        return response(message=f"Article {_id} not found", ok=False), 400

    article = article[0]
    if article.get('user') != get_user()['user_id']:
        return response(message=f"User {get_user()['user_id']} is not the "
                                f"owner of article {_id}", ok=False), 401

    deleted = crud.delete({'id': _id}, 'articles')
    if not deleted.deleted_count:
        return response(message=f"Error deleting article", ok=False), 500
    return response(message=f"Successfully deleted article {_id}",
                    ok=True), 200


@ARTICLES_BP.route('/', methods=['GET'])
def get_article():
    data = crud.get(request.args, 'articles')
    return jsonify({"ok": True, "data": data}), 200


@ARTICLES_BP.route('/', methods=['POST'])
@login_required
def post_article():
    body = request.get_json(silent=True)

    if not body:
        return response("Invalid or empty request body", ok=False), 400

    body['user'] = get_user()['user_id']

    # Optional fields, zero or more. If not present, init them as an empty list
    body.setdefault('pictures', [])
    body.setdefault('payment_methods', [])
    body.setdefault('tags', [])

    return crud.post(
        data=body,
        col='articles',
        attributes=('name', 'description', 'available_units', 'price',
                    'user', 'latitude', 'longitude', 'pictures',
                    'payment_methods', 'tags')
    )
