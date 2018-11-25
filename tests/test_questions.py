def test_list_questions_initially_empty(client):
    resp = client.get('/question/')
    assert not resp.json['data']
    assert isinstance(resp.json['data'], list)
