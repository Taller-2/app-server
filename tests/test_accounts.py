def test_account(client):
    keys = ['user_id', 'email', 'name', '_id']
    resp = client.get('/account/current/')
    assert all(key in resp.json['data'] for key in keys)
