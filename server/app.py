import os

from flask import Flask

from server.libs.mongo import JSONEncoder
from server.logger import logger

ROOT_PATH = os.path.dirname(os.path.realpath(__file__))

LOG = logger.get_root_logger(
    os.environ.get('ROOT_LOGGER', 'root'),
    filename=os.path.join(ROOT_PATH, 'output.log')
)


def create_app(conf='conf.local.Config'):
    LOG.info('running environment: %s', os.environ.get('ENV'))
    # Debug mode if development env
    app = Flask(__name__)

    app.config.from_object(conf)

    from server.libs.mongo import mongo

    mongo.init_app(app)

    from server.routes.root import EXAMPLE_BP
    from server.routes.ping import PING_BP
    from server.routes.articles import ARTICLES_BP
    from server.routes.accounts import ACCOUNTS_BP
    from server.routes.articles_stats import ARTICLE_STATS_BP
    from server.routes.chat_messages import CHAT_MESSAGES_BP
    from server.routes.purchases import PURCHASES_BP
    from server.routes.questions import QUESTIONS_BP
    from server.routes.sales import SALES_BP

    app.register_blueprint(EXAMPLE_BP)
    app.register_blueprint(PING_BP)
    app.register_blueprint(ARTICLES_BP)
    app.register_blueprint(ACCOUNTS_BP)
    app.register_blueprint(ARTICLE_STATS_BP)
    app.register_blueprint(CHAT_MESSAGES_BP)
    app.register_blueprint(PURCHASES_BP)
    app.register_blueprint(QUESTIONS_BP)
    app.register_blueprint(SALES_BP)
    # use the modified encoder class to handle ObjectId and Datetime object
    # while jsonifying the response
    app.json_encoder = JSONEncoder

    return app
