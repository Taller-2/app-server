import os

from flask import Flask

from server.libs.mongo import JSONEncoder
from server.logger import logger

ROOT_PATH = os.path.dirname(os.path.realpath(__file__))

LOG = logger.get_root_logger(
    os.environ.get('ROOT_LOGGER', 'root'),
    filename=os.path.join(ROOT_PATH, 'output.log')
)


def create_app():
    LOG.info('running environment: %s', os.environ.get('ENV'))
    # Debug mode if development env
    app = Flask(__name__)

    app.config.from_object('config.Config')

    from server.libs.mongo import mongo

    mongo.init_app(app)

    from server.routes.root import EXAMPLE_BP
    from server.routes.users import MONGO_TEST, REGISTRATION
    from server.routes.ping import PING_BP
    app.register_blueprint(EXAMPLE_BP)
    app.register_blueprint(MONGO_TEST)
    app.register_blueprint(PING_BP)
    app.register_blueprint(REGISTRATION)

    # use the modified encoder class to handle ObjectId and Datetime object
    # while jsonifying the response
    app.json_encoder = JSONEncoder

    return app
