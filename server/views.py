import os
import json

from flask import send_from_directory, Blueprint
from server import LOG

EXAMPLE_BP = Blueprint('example', __name__, url_prefix='/')


@EXAMPLE_BP.route('/')
def root():
    """ static files serve """
    return json.dumps({
        "test": "Test successful"
    })


@EXAMPLE_BP.errorhandler(404)
def not_found(error):
    """ error handler """
    LOG.error(error)
    # return make_response(jsonify({'error': 'Not found'}), 404)
    return send_from_directory('template', '404.html')


@EXAMPLE_BP.route('/<path:path>')
def static_proxy(path):
    """ static folder serve """
    file_name = path.split('/')[-1]
    dir_name = os.path.join('template', '/'.join(path.split('/')[:-1]))
    return send_from_directory(dir_name, file_name)
