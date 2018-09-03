""" index file for REST APIs using Flask """
import os
from flask import Flask, Blueprint
from .logger import logger


# Create a logger object to log the info and debug
LOG = logger.get_root_logger(os.environ.get(
    'ROOT_LOGGER', 'root'), filename=os.path.join(ROOT_PATH, 'output.log'))


bp = Blueprint('example', __name__, url_prefix='/')
