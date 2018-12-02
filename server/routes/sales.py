from flask import Blueprint, jsonify

from server.decorators.login_required import login_required
from server.model.account import Account
from server.model.purchase import Purchase
from server.routes.purchases import add_payment_and_shipment_status

SALES_BP = Blueprint('sales', __name__, url_prefix='/my_sales')


@SALES_BP.route('/', methods=['GET'])
@login_required
def my_sales():
    return jsonify({
        'data': add_payment_and_shipment_status(
            Purchase.get_by_seller(Account.current())
        ),
        'ok': True
    }), 200
