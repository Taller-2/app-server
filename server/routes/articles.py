from flask import request, Blueprint, jsonify

from server.decorators.login_required import login_required
from server.model.article import Article
from server.model.user import user_id
from server.utils import response

ARTICLES_BP = Blueprint('articles', __name__, url_prefix='/article')


@ARTICLES_BP.route('/<_id>/', methods=['DELETE'])
@login_required
def delete_article(_id):
    try:
        article = Article.get_one(_id)
    except ValueError as e:
        return response(message=str(e), ok=False), 400

    if not article:
        return response(message=f"Article {_id} not found", ok=False), 400

    if article['user'] != user_id():
        return response(message=f"User {user_id()} is not the "
                                f"owner of article {_id}", ok=False), 401

    deleted = article.delete()
    if not deleted.deleted_count:
        return response(message=f"Error deleting article", ok=False), 500
    return response(message=f"Successfully deleted article {_id}",
                    ok=True), 200


@ARTICLES_BP.route('/', methods=['GET'])
def get_article():
    try:
        articles = Article.get_many(**request.args)
    except ValueError:
        received = request.query_string.decode('utf-8')
        return response(message=f"Error parsing querystring parameters. "
                                f"Received '{received}'",
                        ok=False), 400
    except KeyError as e:
        keys = ', '.join(Article.schema.keys())
        return response(message=f"Invalid key {e}. "
                                f"Valid parameters are {keys}",
                        ok=False), 400
    data = [article.to_json() for article in articles]
    return jsonify({"ok": True, "data": data}), 200


@ARTICLES_BP.route('/', methods=['POST'])
@login_required
def post_article():
    body = request.get_json(silent=True)

    if not body:
        return response("Invalid or empty request body", ok=False), 400

    body['user'] = user_id()

    # Optional fields, zero or more. If not present, init them as an empty list
    body.setdefault('pictures', [])
    body.setdefault('payment_methods', [])
    body.setdefault('tags', [])

    try:
        article = Article(body)
    except ValueError as e:
        return response(message=f"Error in validation: {e}", ok=False), 400

    _id = article.save()
    return jsonify({"ok": True, "_id": _id}), 200


@ARTICLES_BP.route('/', methods=['PATCH'])
@login_required
def put_article():
    body = request.get_json(silent=True)

    if not body:
        return response("Invalid or empty request body", ok=False), 400

    _id = body.get('_id')
    if _id is None:
        return response("_id field invalid", ok=False), 400

    try:
        article = Article.get_one(_id)
    except ValueError:
        return response(f'Bad article id: {_id}', ok=False), 400

    try:
        article.update(**body)
    except ValueError as e:
        return response(message=f"Error in validation: {e}", ok=False), 400

    return jsonify({"ok": True, "data": article.to_json()}), 200
