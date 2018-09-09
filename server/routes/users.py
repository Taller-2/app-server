from flask import request, jsonify, Blueprint
from passlib.hash import md5_crypt

from server.model import crud

MONGO_TEST = Blueprint('mongo_test', __name__, url_prefix='/')
REGISTRATION = Blueprint('resgistration', __name__, url_prefix='/')


def user_get(args):
    return crud.get(args, "users")


def user_post(data):
    return crud.post(data, "users")


def user_delete(data):
    if 'email' not in data:
        dicc = {'ok': False, 'message': 'Bad request parameters!'}
        return jsonify(dicc), 400
    db_response = crud.delete(data, "users")
    if db_response.deleted_count == 1:
        response = {'ok': True, 'message': 'record deleted'}
    else:
        response = {'ok': True, 'message': 'no record found'}
    return jsonify(response), 200


def user_patch(data):
    if not crud.patch(data, "users"):
        dicc = {'ok': False, 'message': 'Bad request parameters!'}
        return jsonify(dicc), 400
    return jsonify({'ok': True, 'message': 'record updated'}), 200


@MONGO_TEST.route('/user', methods=['GET', 'POST', 'DELETE', 'PATCH'])
def user():
    if request.method == 'GET':
        return jsonify(user_get(request.args)), 200
    data = request.get_json()
    if request.method == 'POST':
        return user_post(data)
    if request.method == 'DELETE':
        return user_delete(data)
    return user_patch(data)


def hash_password(password):
    return md5_crypt.using(salt_size=4).hash(password)


def check_password(password, password_hash):
    return md5_crypt.verify(password, password_hash)


def authenticate(info):
    data = user_get(info)
    if data is None:
        return "You have not sign up", False
    if data["username"] != info["username"]:
        return "Wrong username", False
    if data["email"] != info["email"]:
        return "Wrong email", False
    if not check_password(info["password"], data["password_hash"]):
        return "Wrong password", False
    return "success authentication", True


@REGISTRATION.route("/login", methods=['POST'])
def login():
    data = request.get_json()
    atributes = ["username", "email", "password"]
    if not all(key in data.keys() for key in atributes):
        return "Missing atributes"
    message, authentication = authenticate(data)
    if not authentication:
        return message
    return jsonify(data), 200


@REGISTRATION.route("/signup", methods=['POST'])
def signup():
    data = request.get_json()
    atributes = [
        "token",
        "username",
        "name",
        "last_name",
        "email",
        "avatar",
        "password"
    ]
    if not all(key in data.keys() for key in atributes):
        return "Missing atributes"
    if len(data.keys()) != len(atributes):
        return "arguments should be: token, username, name, last_name, " \
               "email, avatar, password"
    data_db = user_get(data)
    if data_db is None:
        password_hash = hash_password(data["password"])
        del data["password"]
        data["password_hash"] = password_hash
        user_post(data)
        return "You have been successfully registered"
    return "username already exist"
