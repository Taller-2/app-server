from flask import Blueprint
from server.controllers.article_stats import ArticleStatsController

ARTICLE_STATS_BP = \
    Blueprint('articles_stats', __name__, url_prefix='/article_stats')


@ARTICLE_STATS_BP.route('/', methods=['GET'])
def get_article_stats():
    return ArticleStatsController.get_article_stats()
