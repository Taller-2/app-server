from server.model.base import Model
from server.model.user import user_id


class Account(Model):
    db_name = 'accounts'

    schema = {
        'user_id': str,
        'email': str,
        'name': str
    }

    @classmethod
    def current(cls):
        return cls.get_many(user_id=user_id())[0]
