import json


def test_get_current_account(client):
    keys = ['user_id', 'email', 'name', '_id']
    resp = client.get('/account/current/')
    assert all(key in resp.json['data'] for key in keys)


def test_update_current_account(client):
    email = 'test@test.com'
    name = 'test'
    client.patch('/account/current/', data=json.dumps({
        'email': email,
        'name': name,
    }), content_type='application/json')

    resp = client.get('/account/current/')
    assert resp.json['data']['email'] == email
    assert resp.json['data']['name'] == name
