from faker import Faker
from pytest import raises

from server.controllers.article import ArticleController
from server.model.article import Article


def setup_function():
    fake = Faker()
    teardown_function()
    Article({
        'name': fake.word(),
        'description': fake.sentence(),
        'available_units': fake.pyint(),
        'price': 20.0,
        'latitude': 0.0,
        'longitude': 0.0,
        'user': fake.word(),
    }).save()

    Article({
        'name': fake.word(),
        'description': fake.sentence(),
        'available_units': fake.pyint(),
        'price': 300.0,
        'latitude': 1.0,
        'longitude': 1.0,
        'user': fake.word(),
    }).save()


def test_no_args_fetches_all():
    articles = ArticleController().get_articles()

    assert len(articles) == 2
    assert articles[0]['latitude'] == 0
    assert articles[0]['longitude'] == 0


def test_bad_argument():
    with raises(ValueError):
        ArticleController(garbage=[1]).get_articles()


def test_missing_some_distance_args():
    with raises(ValueError):
        ArticleController(my_lat=[1]).get_articles()


def test_distance_args_bad_type():
    with raises(ValueError):
        ArticleController(my_lat=[1.0],
                          my_lon=[12.0],
                          max_distance=["garbage"]).get_articles()


def test_article_filter_by_distance_no_results():
    articles = ArticleController(my_lat=[15.0],
                                 my_lon=[12.0],
                                 max_distance=[1]).get_articles()

    assert len(articles) == 0


def test_article_filter_by_distance():
    articles = ArticleController(my_lat=[0.0],
                                 my_lon=[0.0],
                                 max_distance=[1]).get_articles()

    assert len(articles) == 1


def teardown_function():
    for a in Article.get_many():
        a.delete()


def test_article_filter_by_price():
    articles = ArticleController(price_min=[300]).get_articles()
    assert len(articles) == 1


def test_article_filter_by_price_and_distance():
    articles = ArticleController(my_lat=[1.0],
                                 my_lon=[1.0],
                                 max_distance=[1],
                                 price_min=[200]).get_articles()

    assert len(articles) == 1
