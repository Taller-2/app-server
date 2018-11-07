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
        'score': Optional[float]
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

    def antiquity(self):
        if not self['created_at']:
            return 0
        return relativedelta(datetime.utcnow(), self['created_at']).years

    def score(self):
        return self['score'] or 0

    def increment_score(self, increment: int):
        self.update(score=self.score() + increment)

    def register_publication(self):
        self.increment_score(1)

    def register_purchase(self):
        self.increment_score(5)

    def register_sale(self):
        self.increment_score(10)
