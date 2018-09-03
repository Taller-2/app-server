import os

import flask


class Config(flask.Config):
    PORT = 4000
    DEBUG = os.environ.get('ENV') == 'development'
    MONGO_URI = os.environ.get('DB', "mongodb://mongodb:27017/todoDev")
