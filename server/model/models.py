from server.libs.mongo import mongo
from server.routes import users

from os import urandom
from base64 import b64encode
from server.wsgi import bcrypt


class User:

    # Class atributes
    users = mongo.db.users
    users_col = "users"

    def __init__(self, username=None, email=None, password=None):
        self.username = username
        self.email = email
        self.password = password
        self.data = {}

    @staticmethod
    def register(username, name, last_name, email, password, avatar):
        data = {
            "id": b64encode(urandom(24)).decode('utf-8'),
            "username": username,
            "name": name,
            "lastName": last_name,
            "email": email,
            "avatar": avatar,
            "password_hash": bcrypt.generate_password_hash(password)
        }
        users.user_post(data, User.users_col)

    def authenticate(self):
        self.data = users.user_get(User.users_col)
        if self.data["username"] != self.username:
            return None
        if self.data["email"] != self.email:
            return None
        a = self.data["password_hash"]
        b = self.password
        password_check = bcrypt.check_password_hash(a, b)
        if not password_check:
            return None



class Message:

    # Class atributes
    messages = mongo.db.messages
    messages_col = "messages"

    def __init__(self, groupid=None, sent_userid=None, content=None):
        self.groupid = groupid
        self.sent_userid = sent_userid
        self.content = content
