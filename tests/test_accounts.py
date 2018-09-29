def test_account(client):
    keys = ['user_id', 'email', 'name']
    resp = client.get('/account/current/')
    assert all(key in resp.json for key in keys)
