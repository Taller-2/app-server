from flask import Blueprint, jsonify

from server.decorators.login_required import login_required
from server.model.account import Account

ACCOUNTS_BP = Blueprint('accounts', __name__, url_prefix='/account')


@ACCOUNTS_BP.route('/current/', methods=['GET'])
@login_required
def current_account():
    return jsonify({"ok": True, "data": Account.current().to_json()}), 200
