from flask import Blueprint, jsonify

from server.decorators.login_required import login_required
from server.model.account import Account
from server.model.purchase import Purchase

SALES_BP = Blueprint('sales', __name__, url_prefix='/my_sales')


@SALES_BP.route('/', methods=['GET'])
@login_required
def my_sales():
    user = Account.current()
    return jsonify({'data': Purchase.get_by_seller(user), 'ok': True}), 200
