from typing import Optional
from server.model.base import Model
from server.controllers.article_stats import ArticleStatsController


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
        if self.action != 'post' and self.action != '':
            current_action = self.action
        ArticleStatsController.save_statistic(current_action, self._data)
        return super(Article, self).save()

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
