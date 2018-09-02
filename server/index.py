""" index file for REST APIs using Flask """
import os
from flask import Flask
from .logger import logger

app = Flask(__name__)

ROOT_PATH = os.path.dirname(os.path.realpath(__file__))

# Create a logger object to log the info and debug
LOG = logger.get_root_logger(os.environ.get(
    'ROOT_LOGGER', 'root'), filename=os.path.join(ROOT_PATH, 'output.log'))

# Port variable to run the server on.
PORT = os.environ.get('PORT')


if __name__ == '__main__':
    LOG.info('running environment: %s', os.environ.get('ENV'))
    # Debug mode if development env
    app.config['DEBUG'] = os.environ.get('ENV') == 'development'
    app.run(host='0.0.0.0', port=int(PORT))  # Run the app
