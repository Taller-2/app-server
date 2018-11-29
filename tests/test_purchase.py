import json
import random

from faker import Faker

from server.model.account import Account
from server.model.article import Article
from server.model.purchase import Purchase

fake = Faker()


def test_get_user_purchases(client):
    resp = client.get('/purchase/')
    assert resp.status_code == 200
    assert not resp.json['data']


def test_post_purchase(client, article):
    resp = client.post('/purchase/', data=json.dumps({
        "article_id": article.get_id(),
        "units": article['available_units'],
        "price": 1000,
        "payment_method": "cash"
    }), content_type='application/json')

    assert resp.status_code == 200

    resp = client.get('/purchase/')
    assert resp.status_code == 200
    article = article.to_json()
    resp_article = resp.json['data'][0]['article']
    for key in article:
        if key == 'available_units':
            assert resp_article[key] == 0  # all units were bought
        else:
            assert resp_article[key] == article[key]


def test_post_bad_article(client):
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
    user_id = 'seller'
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
        'user_id': 'something',
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
    user_id = 'purchaser'
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
        'user_id': user_id,
        'article_id': article_id,
        'units': 1
    }).save()
    assert Account.get_one(purchaser_id).score() == score + 5
    Purchase.get_one(purchase_id).save()
    assert Account.get_one(purchaser_id).score() == score + 5
