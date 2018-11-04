from flask import request, Blueprint, jsonify
from server.model.article_statistics import ArticleStatistics
from server.utils import response

ARTICLE_STATS_BP = \
    Blueprint('articles_stats', __name__, url_prefix='/article_stats')


@ARTICLE_STATS_BP.route('/', methods=['GET'])
def get_article_stats():
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
