

# content of test_sample.py
def inc(x):
    return x + 1


def test_answer():
    assert inc(3) == 4


def test_with_client(client):
    resp = client.get('/')
    assert resp.status_code == 404
