from server.model.base import Model


class UserStatistics(Model):
    db_name = 'user_statistics'

    schema = {
        'name': str,
        'user_id': str,
        'timestamp': str
    }
