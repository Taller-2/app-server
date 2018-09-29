from flask import request, Blueprint, jsonify

from server.decorators.login_required import login_required
from server.libs.mongo import validate_object_id
from server.model.article import Article
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

    article = Article.get_one(_id)

    if not article:
        return response(message=f"Article {_id} not found", ok=False), 400

    if article['user'] != get_user()['user_id']:
        return response(message=f"User {get_user()['user_id']} is not the "
                                f"owner of article {_id}", ok=False), 401

    deleted = article.delete()
    if not deleted.deleted_count:
        return response(message=f"Error deleting article", ok=False), 500
    return response(message=f"Successfully deleted article {_id}",
                    ok=True), 200


@ARTICLES_BP.route('/', methods=['GET'])
def get_article():
    articles = Article.get_many(**request.args)
    data = [article.to_json() for article in articles]
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

    try:
        article = Article(body)
    except ValueError as e:
        return response(message=f"Error in validation: {e}", ok=False), 400

    article.save()
    return response(message=f"Successfully created new article!", ok=True)
