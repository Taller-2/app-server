import json


def test_create_missing_text(client):
    resp = client.post('/chat_message/', data=json.dumps({
        'name': 'name',
        'sender_user_id': 'sender_user_id'
    }), content_type='application/json')
    assert resp.status_code == 400


def test_create_missing_name(client):
    resp = client.post('/chat_message/', data=json.dumps({
        'text': 'text',
        'sender_user_id': 'sender_user_id'
    }), content_type='application/json')
    assert resp.status_code == 400


def test_create_missing_sender_user_id(client):
    resp = client.post('/chat_message/', data=json.dumps({
        'text': 'text',
        'name': 'name',
    }), content_type='application/json')
    assert resp.status_code == 400


def test_find_all(client):
    text = 'text'
    name = 'name'
    sender_user_id = 'sender_user_id'
    client.post('/chat_message/', data=json.dumps({
        'text': text,
        'name': name,
        'sender_user_id': sender_user_id
    }), content_type='application/json')
    resp = client.get('/chat_message/')
    assert resp.json['data'][0]['text'] == text
    assert resp.json['data'][0]['name'] == name
    assert resp.json['data'][0]['sender_user_id'] == sender_user_id
