from flask import Blueprint, request, jsonify

from server.decorators.login_required import login_required
from server.model.account import Account
from server.model.article import Article
from server.model.purchase import Purchase
from server.utils import response, create

PURCHASES_BP = Blueprint('purchases', __name__, url_prefix='/purchase')


@PURCHASES_BP.route('/', methods=['GET'])
@login_required
def get_purchases():
    user = Account.current()
    return jsonify({'data': Purchase.get_for_user(user), 'ok': True}), 200


@PURCHASES_BP.route('/', methods=['POST'])
@login_required
def buy():
    body = request.json
    if body is None:
        return response("Request body is null", ok=False), 400

    article_id = body.get('article_id')

    try:
        article = Article.get_one(article_id)
        if article is None:
            return response("article ID {article_id} not found", ok=False), 400
    except ValueError:
        return response(f"article_id not specified", ok=False), 400

    account_id = Account.current().get_id()
    body['user_id'] = account_id
    return create(Purchase, additional_fields={'user_id': account_id})
