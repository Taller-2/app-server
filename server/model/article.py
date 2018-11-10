from typing import Optional

from server.controllers.article_stats import ArticleStatsController
from server.model.account import Account
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

    def __init__(self, json: dict):
        self.action = ''
        super().__init__(json)

    def save(self):
        current_action = 'post'
        if self.action:
            current_action = self.action
        ArticleStatsController.save_statistic(current_action, self._data)
        account = self.account()
        is_new = self.is_new_instance()
        _id = super(Article, self).save()
        if is_new and account:
            account.register('publication')
        return _id

    def update(self, **values):
        self.action = 'update'
        return super(Article, self).update(**values)

    def delete(self):
        self.action = 'delete'
        ArticleStatsController.save_statistic(self.action, self._data)
        return super(Article, self).delete()

    @classmethod
    def get_many(cls, *_, **kwargs):
        articles = super(Article, cls).get_many(**kwargs)
        for an_article in articles:
            an_article = an_article.to_json()
            ArticleStatsController.save_statistic('get', an_article)
        return articles

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

    def account(self) -> Optional[Account]:
        try:
            return Account.get_many(user_id=self['user'])[0]
        except IndexError:
            return None
