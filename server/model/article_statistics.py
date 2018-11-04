from server.model.base import Model


class ArticleStatistics(Model):
    db_name = 'articles_statistics'

    schema = {
        'name': str,
        'action': str,
        'description': str,
        'price': float,
        'user': str,
        'timestamp': str,
        'latitude': float,
        'longitude': float
    }
