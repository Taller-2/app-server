from typing import Optional, Union
from server.model.base import Model


class Article(Model):
    db_name = 'articles'

    schema = {
        'name': str,
        'description': str,
        'available_units': int,
        'price': Union[int, float],
        'user': str,
        'latitude': Union[int, float],
        'longitude': Union[int, float],
        'pictures': Optional[list],
        'payment_methods': Optional[list],
        'tags': Optional[list]
    }
