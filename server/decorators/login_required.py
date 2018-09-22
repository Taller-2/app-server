from functools import wraps

import google.auth.transport.requests
import google.oauth2.id_token
from flask import request, g, current_app


def login_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if current_app.config['SKIP_AUTH']:
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