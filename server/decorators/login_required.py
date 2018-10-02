from functools import wraps

import google.auth.transport.requests
import google.oauth2.id_token
from flask import request, g, current_app

from server.model.account import Account
from server.utils import response


def mock_user_id() -> str:
    return 'efUoF0bC3lUn4BbzzjKSSz3FkcF2'  # dylanalvarez1995@gmail.com


def get_or_create_account(claims):
    if Account.get_many({'user_id': g.user_id}):
        return
    default_attrs = ['user_id', 'email', 'name']
    Account({attr: claims[attr] for attr in default_attrs}).save()


def get_or_create_mock_account():
    g.user_id = mock_user_id()
    get_or_create_account({
        'user_id': g.user_id,
        'email': 'dylanalvarez1995@gmail.com',
        'name': 'Dylan Alvarez'
    })


def login_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if current_app.config['SKIP_AUTH']:
            get_or_create_mock_account()
            return func(*args, **kwargs)
        if 'HTTP_AUTHORIZATION' not in request.headers.environ:
            return response(message='Unauthorized', ok=False), 401
        claims = google.oauth2.id_token.verify_firebase_token(
            request.headers.environ['HTTP_AUTHORIZATION'],
            google.auth.transport.requests.Request()
        )
        if not claims:
            g.user_id = None
            return response(message='Unauthorized', ok=False), 401
        g.user_id = claims['user_id']
        get_or_create_account(claims)
        return func(*args, **kwargs)

    return decorated_function
