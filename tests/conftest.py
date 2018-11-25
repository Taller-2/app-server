import pytest
from faker import Faker

from server.app import create_app
from server.libs.mongo import mongo
from server.model.article import Article

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
    art = Article({
        "name": fake.pystr(),
        "description": fake.text(),
        "available_units": fake.pyint(),
        "price": fake.pyfloat(),
        "latitude": fake.pyfloat(),
        "longitude": fake.pyfloat(),
        "user": fake.pystr(),
    })
    art.save()
    yield art
    art.delete()
