from datetime import datetime

from server.model.base import Model


class AccountEvent(Model):
    db_name = 'account_events'

    schema = {
        'account_id': str,
        'type': str,
        'article_name': str,
        'score_increment': int,
        'timestamp': datetime
    }

    valid_types = ['publication', 'purchase', 'sale']

    @classmethod
    def validate(cls, json):
        super().validate(json)
        if json.get('type') not in cls.valid_types:
            raise ValueError(f'{json.get("type")} is not a valid type. '
                             f'It must be one of {cls.valid_types}')
