import json

from flask import Blueprint

EXAMPLE_BP = Blueprint('example', __name__, url_prefix='/')


@EXAMPLE_BP.route('/')
def root():
    """ static files serve """
    return json.dumps({
        "test": "Test successful"
    })
