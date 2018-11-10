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


def test_schema_of_updated_article(client):
    post = client.post('/article/', data=json.dumps({
        'price': 1,
        'name': 'nombre',
        'description': 'desc',
        'available_units': 11,
        'latitude': 0,
        'longitude': 0,
        'user': 'fake_user'
    }), content_type='application/json')

    _id = post.json['_id']
    patch = client.patch('/article/', data=json.dumps({
        '_id': _id,
        'price': 100000,
        'name': 'other name'
    }), content_type='application/json')
    assert patch.status_code == 200

    get = client.get('/article_stats/')
    assert get.json['ok']
    print(get.json['data'])
    assert len(get.json['data']) == 2
    assert get.json['data'][1]['name'] == 'other name'
    assert get.json['data'][1]['action'] == 'update'
    assert get.json['data'][1]['description'] == 'desc'
    assert get.json['data'][1]['price'] == 100000
    assert get.json['data'][1]['latitude'] == 0
    assert get.json['data'][1]['longitude'] == 0


def test_schema_of_consulted_articles(client):
    post = client.post('/article/', data=json.dumps({
        'price': 1,
        'name': 'name',
        'description': 'desc',
        'available_units': 11,
        'latitude': 0,
        'longitude': 0,
        'user': 'fake_user'
    }), content_type='application/json')

    assert post.status_code == 200

    get_articles = client.get('/article/')
    assert get_articles.status_code == 200
    assert len(get_articles.json['data']) == 1

    get = client.get('/article_stats/')
    assert get.json['ok']
    assert len(get.json['data']) == 2
    assert get.json['data'][1]['name'] == 'name'
    assert get.json['data'][1]['action'] == 'get'
    assert get.json['data'][1]['description'] == 'desc'
    assert get.json['data'][1]['price'] == 1
    assert get.json['data'][1]['latitude'] == 0
    assert get.json['data'][1]['longitude'] == 0


def test_schema_of_deleted_articles(client):
    post = client.post('/article/', data=json.dumps({
        'price': 1,
        'name': 'name',
        'description': 'desc',
        'available_units': 11,
        'latitude': 0,
        'longitude': 0,
        'user': 'fake_user'
    }), content_type='application/json')

    assert post.status_code == 200
    _id = post.json['_id']

    deleted_article = client.delete(f'/article/{_id}/')
    assert deleted_article.status_code == 200

    get = client.get('/article_stats/')
    assert get.json['ok']
    assert len(get.json['data']) == 2
    assert get.json['data'][1]['name'] == 'name'
    assert get.json['data'][1]['action'] == 'delete'
    assert get.json['data'][1]['description'] == 'desc'
    assert get.json['data'][1]['price'] == 1
    assert get.json['data'][1]['latitude'] == 0
    assert get.json['data'][1]['longitude'] == 0


def test_logged_data_of_posted_article_filter_bad_param(client):
    resp = client.get('/article_stats/?param_not_in_schema=no_name')
    assert resp.status_code, 400


def test_logged_data_of_posted_article_filter_empty_param(client):
    resp = client.get('/article_stats/?name')
    assert resp.status_code, 400
