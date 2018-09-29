from flask import g


def user() -> dict:
    """Returns the Firebase user, initially set in the login_required decorator
    Usually this function should be mocked during tests to manipulate the
    requests' users.
    """
    return g.user
