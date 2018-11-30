from flask import Blueprint, request, jsonify

from server.decorators.login_required import login_required
from server.model.account import Account
from server.model.article import Article
from server.model.purchase import Purchase
from server.model.user import user_id
from server.shared_server import shared_server
from server.shared_server.shared_server import create_payment, create_shipment
from server.utils import response, create

PURCHASES_BP = Blueprint('purchases', __name__, url_prefix='/purchase')


@PURCHASES_BP.route('/', methods=['GET'])
@login_required
def get_purchases():
    user = Account.current()
    purchases = Purchase.get_for_user(user)
    data = []
    for purchase in purchases:
        _response = shared_server.status(purchase['_id']).json()
        if not _response['success']:
            return response(f"shared server: {_response['error']}", ok=False),\
                   400
        data.append({**purchase, **{
            'payment_status': _response['payment_status'],
            'shipment_status': _response['shipment_status']
        }})
    return jsonify({'data': data, 'ok': True}), 200


def after_purchase(price, payment_method, address):
    def callback(purchase):
        payment_response = create_payment(price, payment_method, purchase)
        if purchase['requested_shipment'] and payment_response.ok:
            payment_json = payment_response.json()['payment']
            create_shipment(payment_json['transactionId'], address)

    return callback


def check_required_fields(body):
    if body is None:
        return response("Request body is null", ok=False), 400
    if not body.get('units'):
        return response("units not specified", ok=False), 400
    if not body.get('price'):
        return response("price not specified", ok=False), 400
    if not body.get('payment_method'):
        return response("payment_method not specified", ok=False), 400
    return None


def get_article(body):
    article_id = body.get('article_id')
    try:
        article = Article.get_one(article_id)
        if article is None:
            return None, response("article was not found", ok=False), 400
    except ValueError:
        return None, response(f"article_id not specified", ok=False), 400
    return article, None


@PURCHASES_BP.route('/', methods=['POST'])
@login_required
def buy():
    body = request.json

    error_response = check_required_fields(body)
    if error_response:
        return error_response

    article, error_response = get_article(body)
    if error_response:
        return error_response

    account_id = Account.current().get_id()

    if user_id() == article['user']:
        return response("You can't purchase your own article", ok=False), 400

    article['available_units'] -= body.get('units')
    if article['available_units'] < 0:
        return response("not enough units", ok=False), 400
    article.save()

    return create(
        Purchase,
        additional_fields={
            'user_id': account_id,
            'requested_shipment': bool(body.get('shipment_address'))
        },
        after_save=after_purchase(body.get('price'),
                                  body.get('payment_method'),
                                  body.get('shipment_address'))
    )
