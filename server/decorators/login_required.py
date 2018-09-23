from functools import wraps

import google.auth.transport.requests
import google.oauth2.id_token
from flask import request, g, current_app


def mock_user():
    return {
        'iss': 'https://securetoken.google.com/mercadolibre-dc978',
        'name': 'Dylan Alvarez',
        'picture': 'https://lh4.googleusercontent.com/-i-yd7LDlh7U/'
                   'AAAAAAAAAAI/AAAAAAAAAAA/'
                   'APUIFaPCd40UPy-1JlSIBtcTPbFP888F5g/s96-c/photo.jpg',
        'aud': 'mercadolibre-dc978',
        'auth_time': 1537142814,
        'user_id': 'efUoF0bC3lUn4BbzzjKSSz3FkcF2',
        'sub': 'efUoF0bC3lUn4BbzzjKSSz3FkcF2',
        'iat': 1537733796,
        'exp': 1537737396,
        'email': 'dylanalvarez1995@gmail.com',
        'email_verified': True,
        'firebase': {
            'identities': {
                'google.com': ['108899007745708697393'],
                'email': ['dylanalvarez1995@gmail.com']
            },
            'sign_in_provider': 'google.com'
        }
    }


def login_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if current_app.config['SKIP_AUTH']:
            g.user = mock_user()
            return func(*args, **kwargs)
        if 'HTTP_AUTHORIZATION' not in request.headers.environ:
            return 'Unauthorized', 401
        claims = google.oauth2.id_token.verify_firebase_token(
            request.headers.environ['HTTP_AUTHORIZATION'],
            google.auth.transport.requests.Request()
        )
        if not claims:
            return 'Unauthorized', 401
        g.user = claims
        return func(*args, **kwargs)

    return decorated_function
