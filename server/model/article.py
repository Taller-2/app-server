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

    CATEGORIES = [
        "Tecnología",
        "Belleza y Cuidado Personal",
        "Deportes y Aire Libre",
        "Hogar y Electrodomésticos",
        "Juguetes y Bebés",
        "Libros",
        "Moda",
        "Supermercado",
        "Vehículos",
        "Inmuebles",
        "Servicios",
    ]

    @classmethod
    def validate(cls, json):
        super(Article, cls).validate(json)
        tags = json.get('tags')
        if not tags:
            return

        for tag in tags:
            if tag not in Article.CATEGORIES:
                raise ValueError(f"Invalid category for articles: {tag}")
