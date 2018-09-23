import json


def test_with_client(client):
    resp = client.get('/')
    assert resp.status_code == 200
    assert resp.json['test']


def test_list_articles_initially_empty(client):
    resp = client.get('/article/')
    assert not resp.json
    assert isinstance(resp.json, list)


def test_insert_article(client):
    client.post('/article/', data=json.dumps({
        'price': 1,
        'name': 'nombre',
        'description': 'desc',
        'available_units': 11,
    }), content_type='application/json')
    resp = client.get('/article/')
    assert len(resp.json) == 1


def test_delete_article(client):
    client.post('/article/', data=json.dumps({
        'price': 1,
        'name': 'nombre',
        'description': 'desc',
        'available_units': 11,
    }), content_type='application/json')
    resp = client.get('/article/')
    count = len(resp.json)
    client.delete('/article/' + resp.json[0]['_id']['$oid'] + '/')
    assert len(client.get('/article/').json) == count - 1
