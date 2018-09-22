from flask import Blueprint
from server.utils import response
PING_BP = Blueprint('ping', __name__, url_prefix='/')


@PING_BP.route("/ping")
def ping():
    return response(message='pong', ok=True)

