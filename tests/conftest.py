import pytest
from faker import Faker

from server.app import create_app
from server.libs.mongo import mongo
from server.model.article import Article
from server.model.purchase import Purchase

fake = Faker()


@pytest.fixture
def client():
    app = create_app(conf='conf.test.Config')
    app.config['TESTING'] = True
    client = app.test_client()

    # Clear databases
    mongo.db['articles'].delete_many({})
    mongo.db['articles_statistics'].delete_many({})
    mongo.db['purchases'].delete_many({})
    mongo.db['questions'].delete_many({})
    mongo.db['chat_message'].delete_many({})
    yield client


@pytest.fixture
def article():
    art = generate_article()
    yield art
    art.delete()


def generate_article():
    instance = Article({
        "name": fake.pystr(),
        "description": fake.text(),
        "available_units": fake.pyint(),
        "price": fake.pyfloat(),
        "latitude": fake.pyfloat(),
        "longitude": fake.pyfloat(),
        "user": fake.pystr(),
    })
    instance.save()
    return instance


@pytest.fixture
def purchase():
    article = generate_article()
    instance = Purchase({
        "article_id": article.get_id(),
        "user_id": fake.pystr(),
        "units": fake.pyint(),
    })
    instance.save()
    yield instance
    instance.delete()