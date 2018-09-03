import os

from flask import Flask
from flask_pymongo import PyMongo

from server.libs.mongo import JSONEncoder
from server.logger import logger

ROOT_PATH = os.path.dirname(os.path.realpath(__file__))

LOG = logger.get_root_logger(os.environ.get(
    'ROOT_LOGGER', 'root'), filename=os.path.join(ROOT_PATH, 'output.log'))


def create_app():
    LOG.info('running environment: %s', os.environ.get('ENV'))
    # Debug mode if development env
    app = Flask(__name__)
    app.config.from_object('config.Config')

    from server.libs.mongo import mongo

    mongo.init_app(app)

    from .views import bp
    from .users import mongo_test
    app.register_blueprint(bp)
    app.register_blueprint(mongo_test)

    """ add mongo url to flask config, so that
    flask_pymongo can use it to make connection"""
    app.config['MONGO_URI'] = os.environ.get('DB')
    """ use the modified encoder class to handle ObjectId
    & datetime object while jsonifying the response """
    app.json_encoder = JSONEncoder

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=app.config.get('PORT', 5000))  # Run the app
