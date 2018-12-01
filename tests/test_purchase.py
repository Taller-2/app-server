import json
import random
from unittest import mock

from faker import Faker

from server.model.account import Account
from server.model.article import Article
from server.model.purchase import Purchase

fake = Faker()

user_id = '5c02f0a28b06dfc832066592'


def test_get_user_purchases(client):
    resp = client.get('/purchase/')
    assert resp.status_code == 200
    assert not resp.json['data']


def test_post_purchase(client, article):
    with mock.patch('server.shared_server.shared_server.request'):
        resp = client.post('/purchase/', data=json.dumps({
            "article_id": article.get_id(),
            "units": article['available_units'],
            "price": 1000,
            "payment_method": "cash"
        }), content_type='application/json')

        assert resp.status_code == 200
        resp_article = Article.get_one(article.get_id()).to_json()
        article = article.to_json()
        for key in article:
            if key == 'available_units':
                assert resp_article[key] == 0  # all units were bought
            else:
                assert resp_article[key] == article[key]


def test_post_bad_article(client):
    with mock.patch('server.shared_server.shared_server.request'):
        resp = client.post('/purchase/', data=json.dumps({
            "units": 1,
        }), content_type='application/json')

        assert resp.status_code == 400


def test_first_save_registers_sale():
    for account in Account.get_many():
        account.delete()
    for article in Article.get_many():
        article.delete()
    for purchase in Purchase.get_many():
        purchase.delete()
    score = random.randint(0, 100)
    seller_id = Account({
        'user_id': user_id,
        'email': fake.email(),
        'name': fake.sentence(),
        'score': score
    }).save()
    article_id = Article({
        'name': fake.word(),
        'description': fake.sentence(),
        'available_units': fake.pyint(),
        'price': 20.0,
        'latitude': 0.0,
        'longitude': 0.0,
        'user': user_id,
    }).save()
    score = Account.get_one(seller_id).score()
    purchase_id = Purchase({
        'user_id': user_id,
        'article_id': article_id,
        'units': 1
    }).save()
    assert Account.get_one(seller_id).score() == score + 10
    Purchase.get_one(purchase_id).save()
    assert Account.get_one(seller_id).score() == score + 10


def test_first_save_registers_purchase():
    for account in Account.get_many():
        account.delete()
    for article in Article.get_many():
        article.delete()
    for purchase in Purchase.get_many():
        purchase.delete()
    score = random.randint(0, 100)
    purchaser_id = Account({
        'user_id': user_id,
        'email': fake.email(),
        'name': fake.sentence(),
        'score': score
    }).save()
    article_id = Article({
        'name': fake.word(),
        'description': fake.sentence(),
        'available_units': fake.pyint(),
        'price': 20.0,
        'latitude': 0.0,
        'longitude': 0.0,
        'user': 'someone else',
    }).save()
    purchase_id = Purchase({
        'user_id': purchaser_id,
        'article_id': article_id,
        'units': 1
    }).save()
    assert Account.get_one(purchaser_id).score() == score + 5
    Purchase.get_one(purchase_id).save()
    assert Account.get_one(purchaser_id).score() == score + 5
