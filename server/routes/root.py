from flask import Blueprint, jsonify
import requests
from server.utils import get_shared_server_auth_header

EXAMPLE_BP = Blueprint('example', __name__, url_prefix='/')


@EXAMPLE_BP.route('/')
def root():
    return jsonify({"test": "Test successful"})


# Shared server request example
@EXAMPLE_BP.route('/payments')
def payments():
    response = requests.get("http://localhost:5000/payments",
                            headers=get_shared_server_auth_header())
    return jsonify({"test": response.json()})
