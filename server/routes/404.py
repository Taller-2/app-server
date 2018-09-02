import os

from flask import send_from_directory

from server.index import app, ROOT_PATH
from server.logger import logger

LOG = logger.get_root_logger(os.environ.get(
    'ROOT_LOGGER', 'root'), filename=os.path.join(ROOT_PATH, 'output.log'))


@app.errorhandler(404)
def not_found(error):
    """ error handler """
    LOG.error(error)
    # return make_response(jsonify({'error': 'Not found'}), 404)
    return send_from_directory('template', '404.html')

