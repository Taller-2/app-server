import json

def test_log_insert_article_info(client):
    client.post('/article/', data=json.dumps({
        'price': 1,
        'name': 'nombre',
        'description': 'desc',
        'available_units': 11,
        'latitude': 0,
        'longitude': 0,
        'user': 'fake_user'
    }), content_type='application/json')
    resp = client.get('/article_statistics/')
    assert len(resp.json['data']) == 1
    assert resp.json['data'][0]['name'] == 'nombre'
