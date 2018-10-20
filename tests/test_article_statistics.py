import json

def test_log_data_of_inserted_article(client):
    client.post('/article/', data=json.dumps({
        'price': 1,
        'name': 'nombre',
        'description': 'desc',
        'available_units': 11,
        'latitude': 0,
        'longitude': 0,
        'user': 'fake_user'
    }), content_type='application/json')
    resp = client.get('/article_stats/')
    assert len(resp.json['data']) == 1


def test_schema_of_logeed_data_of_inserted_article(client):
    client.post('/article/', data=json.dumps({
        'price': 1,
        'name': 'nombre',
        'description': 'desc',
        'available_units': 11,
        'latitude': 0,
        'longitude': 0,
        'user': 'fake_user'
    }), content_type='application/json')
    resp = client.get('/article_stats/')
    assert resp.json['ok']
    assert len(resp.json['data']) == 1
    assert resp.json['data'][0]['name'] == 'nombre'
    assert resp.json['data'][0]['action'] == 'post'
    assert resp.json['data'][0]['description'] == 'desc'
    assert resp.json['data'][0]['price'] == 1
    assert resp.json['data'][0]['latitude'] == 0
    assert resp.json['data'][0]['longitude'] == 0


def test_message_i(client):
    client.post('/article/', data=json.dumps({
        'price': 1,
        'name': 'nombre',
        'description': 'desc',
        'available_units': 11,
        'latitude': 0,
        'longitude': 0,
        'user': 'fake_user'
    }), content_type='application/json')
    resp = client.get('/article_stats/')
    assert resp.json['ok']
    assert len(resp.json['data']) == 1
    assert resp.json['data'][0]['name'] == 'nombre'
    assert resp.json['data'][0]['action'] == 'post'
    assert resp.json['data'][0]['description'] == 'desc'
    assert resp.json['data'][0]['price'] == 1
    assert resp.json['data'][0]['latitude'] == 0
    assert resp.json['data'][0]['longitude'] == 0


def test_logged_data_of_posted_article_filter_bad_param(client):
    resp = client.get('/article_stats/?param_not_in_schema=no_name')
    assert resp.status_code, 400


def test_logged_data_of_posted_article_filter_empty_param(client):
    resp = client.get('/article_stats/?name')
    assert resp.status_code, 400
