import time
import datetime
from flask import request, jsonify

from server.utils import response
from server.model.article_statistics import ArticleStatistics


class ArticleStatsController:

    @classmethod
    def save_statistic(cls, action, article_data):
        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        body = {}
        for key in article_data.keys():
            if key not in ArticleStatistics.schema.keys():
                continue
            body[key] = article_data[key]
        body['action'] = action
        body['timestamp'] = st
        article_statistics = ArticleStatistics(body)
        article_statistics.save()
        return

    @classmethod
    def get_article_stats(cls):
        try:
            articles_statistics = ArticleStatistics.get_many(**request.args)
        except ValueError:
            received = request.query_string.decode('utf-8')
            return response(message=f"Error parsing querystring parameters. "
                                    f"Received '{received}'",
                            ok=False), 400
        except KeyError as e:
            keys = ', '.join(ArticleStatistics.schema.keys())
            return response(message=f"Invalid key {e}. "
                                    f"Valid parameters are {keys}",
                            ok=False), 400
        data = [article.to_json() for article in articles_statistics]
        return jsonify({"ok": True, "data": data}), 200
