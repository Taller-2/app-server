from typing import Optional
from server.model.base import Model


class Article(Model):
    db_name = 'articles'

    schema = {
        'name': str,
        'description': str,
        'available_units': int,
        'price': float,
        'user': str,
        'latitude': float,
        'longitude': float,
        'pictures': Optional[list],
        'payment_methods': Optional[list],
        'tags': Optional[list]
    }
