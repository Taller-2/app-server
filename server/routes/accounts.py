from flask import Blueprint, g, jsonify

from server.decorators.login_required import login_required

ACCOUNTS_BP = Blueprint('accounts', __name__, url_prefix='/account')


@ACCOUNTS_BP.route('/current/', methods=['GET'])
@login_required
def current_account():
    keys = ['user_id', 'email', 'name', 'picture']
    return jsonify({key: g.user[key] for key in keys})
