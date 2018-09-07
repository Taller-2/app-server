from flask import Blueprint

PING_BP = Blueprint('ping', __name__, url_prefix='/')


@PING_BP.route("/ping")
def ping():
    return "pong"
