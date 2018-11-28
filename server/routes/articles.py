from datetime import datetime

from flask import request, Blueprint, jsonify

from server.controllers.article import ArticleController
from server.decorators.login_required import login_required
from server.model.account import Account
from server.model.article import Article
from server.model.question import Question
from server.model.user import user_id
from server.shared_server import shared_server
from server.utils import find_all, create, response, patch

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


@ARTICLES_BP.route('/<_id>/', methods=['GET'])
def get_single_article(_id):
    try:
        return jsonify(Article.get_one(_id).to_json())
    except ValueError:
        return response(f"invalid id {_id}",
                        ok=False), 400


@ARTICLES_BP.route('/<_id>/shipment_cost/', methods=['GET'])
@login_required
def shipment_cost(_id):
    args = request.args
    lat = args.get('my_lat')
    lon = args.get('my_lon')
    if not (lat and lon):
        return response(message=f"latitude and longitude missing",
                        ok=False), 400
    try:
        lat = float(lat)
        lon = float(lon)
    except ValueError:
        return response(message="latitude and longitude must be numbers",
                        ok=False), 400
    try:
        article = Article.get_one(_id)
    except ValueError as e:
        return response(message=str(e), ok=False), 400
    if not article:
        return response(message=f"Article {_id} not found", ok=False), 400
    cash_response = shared_server.shipment_cost(
        article, lat, lon, 'cash'
    )
    credit_response = shared_server.shipment_cost(
        article, lat, lon, 'credit'
    )
    debit_response = shared_server.shipment_cost(
        article, lat, lon, 'debit'
    )
    cash_data = cash_response.json()
    credit_data = credit_response.json()
    debit_data = debit_response.json()
    ok = cash_data["success"]
    ok = ok and credit_data["success"]
    ok = ok and debit_data["success"]
    return jsonify({
        'ok': ok,
        'data': {
            'cash': cash_data["cost"],
            'credit': credit_data["cost"],
            'debit': debit_data["cost"]
        }
    }), 200 if ok else 500


@ARTICLES_BP.route('/', methods=['GET'])
def get_article():
    return find_all(
        Article,
        get_instances=lambda: ArticleController(**request.args).get_articles()
    )


@ARTICLES_BP.route('/', methods=['POST'])
@login_required
def post_article():
    return create(Article,
                  optional_fields=['pictures', 'payment_methods', 'tags'],
                  additional_fields={'user': user_id()})


@ARTICLES_BP.route('/', methods=['PATCH'])
@login_required
def put_article():
    return patch(Article)


@ARTICLES_BP.route('/categories/', methods=['GET'])
def list_categories():
    return jsonify({'categories': Article.CATEGORIES}), 200


@ARTICLES_BP.route('/<_id>/question/', methods=['GET'])
def questions(_id):
    try:
        article = Article.get_one(_id)
    except ValueError as e:
        return response(message=str(e), ok=False), 400

    if not article:
        return response(message=f"Article {_id} not found", ok=False), 400

    return jsonify({
        'data': [q.to_json() for q in Question.get_many(article_id=_id)],
        'ok': True
    })


@ARTICLES_BP.route('/<_id>/question/', methods=['POST'])
@login_required
def create_question(_id):
    try:
        article = Article.get_one(_id)
    except ValueError as e:
        return response(message=str(e), ok=False), 400

    if not article:
        return response(message=f"Article {_id} not found", ok=False), 400

    return create(Question,
                  additional_fields={'created_at': datetime.utcnow(),
                                     'article_id': _id,
                                     'user_id': Account.current().get_id()})


@ARTICLES_BP.route('/<article_id>/question/<question_id>/', methods=['POST'])
@login_required
def answer_question(article_id, question_id):
    try:
        article = Article.get_one(article_id)
    except ValueError as e:
        return response(message=str(e), ok=False), 400

    if not article:
        return response(message=f"Article {article_id} not found",
                        ok=False), 400

    try:
        question = Question.get_one(question_id)
    except ValueError as e:
        return response(message=str(e), ok=False), 400

    body = request.get_json(silent=True)
    if not body:
        return response("Invalid or empty request body", ok=False), 400

    answer = body.get('answer')
    if not answer:
        return response("No answer specified", ok=False), 400

    answered_at = datetime.utcnow()

    question.update(**{'answer': answer, 'answered_at': answered_at})
    return jsonify({"ok": True, "data": question.to_json()}), 200
