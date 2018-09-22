from flask import request, Blueprint, jsonify

from server.decorators.login_required import login_required
from server.model import crud
from server.utils import response

ARTICLES_BP = Blueprint('articles', __name__, url_prefix='/article')


@ARTICLES_BP.route('/<_id>/', methods=['DELETE'])
def delete_article(_id):
    deleted = crud.delete({'id': _id}, 'articles')

    if not deleted.deleted_count:
        return response(message=f"Article {_id} not found", ok=False), 400
    return response(message=f"Successfully deleted article {_id}", ok=True), 200


@ARTICLES_BP.route('/', methods=['GET'])
def get_article():
    data = crud.get(request.args, 'articles')
    return jsonify({"ok": True, "data": data}), 200


@login_required
@ARTICLES_BP.route('/', methods=['POST'])
def post_article():
    body = request.get_json(silent=True)

    if not body:
        return response("Invalid or empty request body", ok=False), 400

    return crud.post(
        request.get_json(),
        'articles',
        ('name', 'description', 'available_units', 'price')
    )
