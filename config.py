import os

import flask


class Config(flask.Config):
    DEBUG = os.environ.get('ENV') == 'development'
    MONGO_URI = os.environ.get('DB', "mongodb://mongodb:27017/development")
