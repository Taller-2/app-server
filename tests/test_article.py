import json
import random
from unittest import mock

import requests_mock
from faker import Faker

from server.model.account import Account
from server.model.article import Article
from server.shared_server.shared_server import URL as shared_server_url

fake = Faker()


def test_with_client(client):
    resp = client.get('/')
    assert resp.status_code == 200
    assert resp.json['test']


def test_list_articles_initially_empty(client):
    resp = client.get('/article/')
    assert not resp.json['data']
    assert isinstance(resp.json['data'], list)


def test_insert_article(client):
    client.post('/article/', data=json.dumps({
        'price': 1,
        'name': 'nombre',
        'description': 'desc',
        'available_units': 11,
        'latitude': 0,
        'longitude': 0,
        'user': 'fake_user'
    }), content_type='application/json')
    resp = client.get('/article/')
    assert len(resp.json['data']) == 1


def test_delete_article(client):
    client.post('/article/', data=json.dumps({
        'price': 1,
        'name': 'nombre',
        'description': 'desc',
        'available_units': 11,
        'latitude': 0,
        'longitude': 0,
    }), content_type='application/json')
    resp = client.get('/article/')
    count = len(resp.json['data'])
    client.delete('/article/' + resp.json['data'][0]['_id'] + '/')
    assert len(client.get('/article/').json['data']) == count - 1


def test_delete_article_unauthorized(client):
    client.post('/article/', data=json.dumps({
        'price': 1,
        'name': 'nombre',
        'description': 'desc',
        'available_units': 11,
        'latitude': 0,
        'longitude': 0,
    }), content_type='application/json')
    resp = client.get('/article/')
    uri = '/article/' + resp.json['data'][0]['_id'] + '/'
    with mock.patch('server.routes.articles.user_id') as fake_user_id:
        fake_user_id.return_value = 'other_user'
        resp = client.delete(uri)
    assert resp.status_code == 401


def test_delete_article_wrong_id(client):
    bad_id = 'fafafafafafafafafafafafa'  # fake mongo 24-char hex string
    resp = client.delete(f'/article/{bad_id}/')
    assert resp.status_code == 400


def test_delete_article_invalid_id(client):
    bad_id = "not hex wrong len"
    resp = client.delete(f'/article/{bad_id}/')
    assert resp.status_code == 400


def test_post_article_invalid_schema(client):
    resp = client.post('/article/', data=json.dumps({
        'price': 1,
        'name': 'nombre',
        'description': 1,  # Bad type, should be str
        'available_units': 11,
        'latitude': 0,
        'longitude': 0,
    }), content_type='application/json')

    assert resp.status_code == 400


def test_post_article_invalid_schema_in_optional_field(client):
    resp = client.post('/article/', data=json.dumps({
        'price': 1,
        'name': 'nombre',
        'description': "desc",
        'available_units': 11,
        'latitude': 0,
        'longitude': 0,
        'tags': "this one has to be a list, but its a string!"
    }), content_type='application/json')

    assert resp.status_code == 400


def test_post_article_empty_body(client):
    resp = client.post('/article/')
    assert resp.status_code == 400


def test_article_filter(client):
    client.post('/article/', data=json.dumps({
        'price': 1,
        'name': 'nombre',
        'description': "desc",
        'available_units': 11,
        'latitude': 0,
        'longitude': 0,
    }), content_type='application/json')

    client.post('/article/', data=json.dumps({
        'price': 1,
        'name': 'second_name',
        'description': "desc",
        'available_units': 11,
        'latitude': 0,
        'longitude': 0,
    }), content_type='application/json')

    resp = client.get('/article/?name=second_name')

    assert len(resp.json['data']) == 1
    assert resp.json['data'][0]['name'] == 'second_name'


def test_article_filter_bad_param(client):
    resp = client.get('/article/?param_not_in_schema=second_name')
    assert resp.status_code, 400


def test_article_filter_empty_param(client):
    resp = client.get('/article/?name')
    assert resp.status_code, 400


def test_article_filter_or(client):
    client.post('/article/', data=json.dumps({
        'price': 1,
        'name': 'nombre',
        'description': "desc",
        'available_units': 11,
        'latitude': 0,
        'longitude': 0,
    }), content_type='application/json')

    client.post('/article/', data=json.dumps({
        'price': 1,
        'name': 'second_name',
        'description': "desc",
        'available_units': 11,
        'latitude': 0,
        'longitude': 0,
    }), content_type='application/json')

    resp = client.get('/article/?name=second_name&name=nombre')

    assert len(resp.json['data']) == 2


def test_article_filter_and(client):
    client.post('/article/', data=json.dumps({
        'price': 1,
        'name': 'nombre',
        'description': "desc",
        'available_units': 11,
        'latitude': 0,
        'longitude': 0,
    }), content_type='application/json')

    client.post('/article/', data=json.dumps({
        'price': 1,
        'name': 'second_name',
        'description': "desc",
        'available_units': 11,
        'latitude': 0,
        'longitude': 0,
    }), content_type='application/json')

    resp = client.get('/article/?name=second_name&price=1')

    assert len(resp.json['data']) == 1
    assert resp.json['data'][0]['name'] == 'second_name'


def test_article_patch_empty(client):
    resp = client.patch('/article/')
    assert resp.status_code == 400


def test_article_patch_invalid(client):
    resp = client.patch('/article/', data='not even json')
    assert resp.status_code == 400


def test_article_patch_no_id(client):
    resp = client.patch('/article/', data=json.dumps({
        'price': 1,
    }), content_type='application/json')
    assert resp.status_code == 400


def test_patch_bad_field(client):
    client.post('/article/', data=json.dumps({
        'price': 1,
        'name': 'nombre',
        'description': "desc",
        'available_units': 11,
        'latitude': 0,
        'longitude': 0,
    }), content_type='application/json')

    resp = client.patch('/article/', data=json.dumps({
        '_id': 'badidsbadidsbadidsbadidsbadidsbadids',
        'name': 'new name',
    }), content_type='application/json')

    assert resp.status_code == 400


def test_patch_bad_type(client):
    post = client.post('/article/', data=json.dumps({
        'price': 1,
        'name': 'nombre',
        'description': "desc",
        'available_units': 11,
        'latitude': 0,
        'longitude': 0,
    }), content_type='application/json')

    _id = post.json['_id']
    resp = client.patch('/article/', data=json.dumps({
        '_id': _id,
        'name': 1,
    }), content_type='application/json')

    assert resp.status_code == 400


def test_article_patch(client):
    post = client.post('/article/', data=json.dumps({
        'price': 1,
        'name': 'nombre',
        'description': "desc",
        'available_units': 11,
        'latitude': 0,
        'longitude': 0,
    }), content_type='application/json')

    _id = post.json['_id']
    resp = client.patch('/article/', data=json.dumps({
        '_id': _id,
        'name': 'new name',
    }), content_type='application/json')

    assert resp.status_code == 200

    get = client.get('/article/')
    assert get.json['data'][0]['name'] == 'new name'


def test_get_categories(client):
    resp = client.get('/article/categories/')
    assert resp.json['categories'] == Article.CATEGORIES


def post_invalid_category(client):
    post = client.post('/article/', data=json.dumps({
        'price': 1,
        'name': 'nombre',
        'description': "desc",
        'available_units': 11,
        'latitude': 0,
        'longitude': 0,
        'tags': ['bad_tag']
    }), content_type='application/json')
    assert post.status_code == 400


def test_get_single_article(client):
    client.post('/article/', data=json.dumps({
        'price': 1,
        'name': 'nombre',
        'description': "desc",
        'available_units': 11,
        'latitude': 0,
        'longitude': 0,
    }), content_type='application/json')

    resp = client.get('/article/').json
    _id = resp["data"][0]["_id"]

    resp = client.get(f'/article/{_id}/')

    assert resp.status_code == 200
    assert resp.json['_id'] == _id


def test_shipment_cost_no_coordinates(client):
    article_id = Article({
        'name': fake.word(),
        'description': fake.sentence(),
        'available_units': fake.pyint(),
        'price': 20.0,
        'latitude': 0.0,
        'longitude': 0.0,
        'user': fake.word(),
    }).save()
    response = client.get(f'/article/{article_id}/shipment_cost/?'
                          f'payment_method=cash')
    assert response.status_code == 400
    assert not response.json['ok']


def test_shipment_cost_non_numeric_coordinates(client):
    article_id = Article({
        'name': fake.word(),
        'description': fake.sentence(),
        'available_units': fake.pyint(),
        'price': 20.0,
        'latitude': 0.0,
        'longitude': 0.0,
        'user': fake.word(),
    }).save()
    response = client.get(f'/article/{article_id}/shipment_cost/?'
                          f'payment_method=cash&'
                          f'my_lat=qwe&my_lon=fds')
    assert response.status_code == 400
    assert not response.json['ok']


def test_shipment_cost(client):
    shared_server_response = {
        "success": True,
        "cost": {
            'cost': 12.0,
            'status': 'enabled'
        }
    }
    shared_server_response_json_data =\
        json.dumps(shared_server_response['cost'], sort_keys=True)
    article_id = Article({
        'name': fake.word(),
        'description': fake.sentence(),
        'available_units': fake.pyint(),
        'price': 20.0,
        'latitude': 0.0,
        'longitude': 0.0,
        'user': fake.word(),
    }).save()
    with requests_mock.Mocker() as _mock:
        _mock.post(f'{shared_server_url}shipment-cost',
                   json=shared_server_response)
        response = client.get(f'/article/{article_id}/shipment_cost/?'
                              f'payment_method=cash&'
                              f'my_lat=0&my_lon=0')
        my_response_json_data = json.dumps(response.json['data'],
                                           sort_keys=True)
        assert response.json['ok']
        assert my_response_json_data == json.dumps({
            "cash": {"cost": 12.0, "status": "enabled"},
            "credit": {"cost": 12.0, "status": "enabled"},
            "debit": {"cost": 12.0, "status": "enabled"}
        }, sort_keys=True)


def test_get_single_article_bad_id(client):
    _id = 'bad_id'
    resp = client.get(f'/article/{_id}/')

    assert resp.status_code == 400


def test_first_save_registers_publication():
    for account in Account.get_many():
        account.delete()
    for article in Article.get_many():
        article.delete()
    user_id = 'user_id'
    score = random.randint(0, 100)
    account_id = Account({
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
    assert Account.get_one(account_id).score() == score + 1
    Article.get_one(article_id).save()
    assert Account.get_one(account_id).score() == score + 1
