from datetime import datetime
from typing import Optional

from dateutil.relativedelta import relativedelta

from server.model.base import Model
from server.model.user import user_id


class Account(Model):
    db_name = 'accounts'

    schema = {
        'user_id': str,
        'email': str,
        'name': str,
        'profile_picture_url': Optional[str],
        'created_at': Optional[datetime],
        'score': Optional[float],
        'instance_id': Optional[str],
    }

    def to_json(self):
        return {
            **super(Account, self).to_json(),
            **{'score': self.score()}
        }

    @classmethod
    def current(cls) -> 'Account':
        return cls.get_many(user_id=user_id())[0]

    def save(self):
        if not self['created_at']:
            self['created_at'] = datetime.utcnow()
        if not self['score']:
            self['score'] = 0
        return super(Account, self).save()

    def antiquity(self) -> int:
        if not self['created_at']:
            return 0
        return relativedelta(datetime.utcnow(), self['created_at']).years

    def score(self) -> float:
        return self['score'] or 0

    def register(self, event: str):
        increment = {
            'publication': 1,
            'purchase': 5,
            'sale': 10,
        }[event]
        self.update(score=self.score() + increment)
