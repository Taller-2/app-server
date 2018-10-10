from flask import request, Blueprint, jsonify

from server.decorators.login_required import login_required
from server.model.account import Account
from server.utils import response

ACCOUNTS_BP = Blueprint('accounts', __name__, url_prefix='/account')


@ACCOUNTS_BP.route('/current/', methods=['GET'])
@login_required
def current_account():
    return jsonify({"ok": True, "data": Account.current().to_json()}), 200


@ACCOUNTS_BP.route('/current/', methods=['PATCH'])
@login_required
def update_current_account():
    body = request.get_json(silent=True)

    if not body:
        return response("Invalid or empty request body", ok=False), 400

    account = Account.current()
    account['email'] = body['email']
    account['name'] = body['name']
    account['profile_picture_url'] = body['profile_picture_url']
    account.save()

    return response(message="Successfully updated current account!", ok=True)
