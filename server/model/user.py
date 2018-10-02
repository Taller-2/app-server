from flask import g


def user_id() -> str:
    """Returns the Firebase user_id, set in the login_required decorator
    Usually this function should be mocked during tests to manipulate the
    requests' users.
    """
    return g.user_id
