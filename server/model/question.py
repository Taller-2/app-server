from datetime import datetime
from typing import Optional

from server.model.base import Model


def iso8601(timestamp: datetime):
    return timestamp.strftime("%Y-%m-%dT%H:%M:%S.%f")


class Question(Model):
    db_name = 'questions'

    schema = {
        'user_id': str,
        'article_id': str,
        'question': str,
        'answer': Optional[str],
        'created_at': datetime,
        'answered_at': Optional[datetime],
    }

    field_formats = {
        'created_at': iso8601,
        'answered_at': lambda x: iso8601(x) if x else str(x),
    }
