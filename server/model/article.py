from typing import Optional
import time
import datetime
from server.model.base import Model
from server.model.article_statistics import ArticleStatistics


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

    def save_statistic(self, action):
        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        body = {}
        for key in self._data.keys():
            if key not in ArticleStatistics.schema.keys():
                continue
            body[key] = self._data[key]
        body['action'] = action
        body['timestamp'] = st
        article_statistics = ArticleStatistics(body)
        article_statistics.save()

    def save(self):
        self.save_statistic('post')
        return super(Article, self).save()
