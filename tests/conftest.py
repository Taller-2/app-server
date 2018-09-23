import pytest
from server.libs.mongo import mongo

from server.app import create_app


@pytest.fixture
def client():
    app = create_app(conf='conf.test.Config')
    app.config['TESTING'] = True
    client = app.test_client()

    # Clear databases
    mongo.db['articles'].delete_many({})
    yield client

