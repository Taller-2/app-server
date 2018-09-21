from functools import wraps

import google.auth.transport.requests
import google.oauth2.id_token
from flask import request, g


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'HTTP_AUTHORIZATION' not in request.headers.environ:
            return 'Unauthorized', 401
        claims = google.oauth2.id_token.verify_firebase_token(
            request.headers.environ['HTTP_AUTHORIZATION'],
            google.auth.transport.requests.Request()
        )
        if not claims:
            return 'Unauthorized', 401
        g.user = claims
        return f(*args, **kwargs)

    return decorated_function
