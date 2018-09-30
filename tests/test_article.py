import json
from unittest import mock


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
    with mock.patch('server.routes.articles.user') as fake_user:
        fake_user.return_value = {'user_id': 'other_user'}
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
