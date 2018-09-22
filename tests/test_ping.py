
def test_ping(client):
    resp = client.get('/ping')

    assert resp.data == b'pong'

