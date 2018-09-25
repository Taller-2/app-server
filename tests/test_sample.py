import json


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
        'user': 'fake_user'
    }), content_type='application/json')
    resp = client.get('/article/')
    count = len(resp.json['data'])
    client.delete('/article/' + resp.json['data'][0]['_id'] + '/')
    assert len(client.get('/article/').json['data']) == count - 1
