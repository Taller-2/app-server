import json
import random
from datetime import datetime

from faker import Faker
from freezegun import freeze_time

from server.model.account import Account

fake = Faker()


def account(extra_attrs: dict = None) -> Account:
    attrs = {
        'user_id': fake.word(),
        'email': fake.email(),
        'name': fake.sentence()
    }
    if extra_attrs is not None:
        attrs = {**attrs, **extra_attrs}
    _id = Account(attrs).save()
    return Account.get_one(_id)


def test_get_current_account(client):
    keys = ['user_id', 'email', 'name', '_id']
    resp = client.get('/account/current/')
    assert all(key in resp.json['data'] for key in keys)


def test_update_current_account(client):
    email = 'test@test.com'
    name = 'test'
    profile_picture_url = 'test.png'
    client.patch('/account/current/', data=json.dumps({
        'email': email,
        'name': name,
        'profile_picture_url': profile_picture_url
    }), content_type='application/json')

    resp = client.get('/account/current/')
    assert resp.json['data']['email'] == email
    assert resp.json['data']['name'] == name
    assert resp.json['data']['profile_picture_url'] == profile_picture_url


@freeze_time("2012-01-01")
def test_save_sets_defaults():
    _account = account()
    assert _account['score'] == 0
    assert _account['created_at'] == datetime.utcnow()


@freeze_time("2012-01-01")
def test_antiquity():
    _account = account({'created_at': datetime(2010, 1, 1)})
    assert _account.antiquity() == 2012 - 2010


def test_score():
    score = 10
    _account = account({'score': score})
    assert _account.score() == _account['score'] == 10


def test_register_publication():
    _account = account({'score': random.randint(0, 100)})
    previous_score = _account.score()
    _account.register('publication', 'article_name')
    assert Account.get_one(_account.get_id()).score() == previous_score + 1


def test_register_purchase():
    _account = account({'score': random.randint(0, 100)})
    previous_score = _account.score()
    _account.register('purchase', 'article_name')
    assert Account.get_one(_account.get_id()).score() == previous_score + 5


def test_register_sale():
    _account = account({'score': random.randint(0, 100)})
    previous_score = _account.score()
    _account.register('sale', 'article_name')
    assert Account.get_one(_account.get_id()).score() == previous_score + 10
