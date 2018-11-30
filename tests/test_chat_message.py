import json
from unittest import mock

from server.model.chat_message import ChatMessage


def test_create_missing_text(client):
    resp = client.post('/chat_message/test_room/', data=json.dumps({
        'name': 'name',
        'sender_user_id': 'sender_user_id',
    }), content_type='application/json')
    assert resp.status_code == 400


def test_find_all(client):
    text = 'text'
    client.post('/chat_message/test_room/', data=json.dumps({
        'text': text,
    }), content_type='application/json')
    resp = client.get('/chat_message/test_room/')
    assert resp.json['data'][0]['text'] == text


def test_multiple_chat_rooms(client):
    text = 'first text'
    client.post('/chat_message/test_room/', data=json.dumps({
        'text': text,
    }), content_type='application/json')
    other_text = 'second text'
    client.post('/chat_message/other_test_room/', data=json.dumps({
        'text': other_text,
    }), content_type='application/json')

    resp = client.get('/chat_message/test_room/')
    assert len(resp.json['data']) == 1
    assert resp.json['data'][0]['text'] == text

    resp = client.get('/chat_message/other_test_room/')
    assert len(resp.json['data']) == 1
    assert resp.json['data'][0]['text'] == other_text


def test_send_with_purchase_id(client, purchase):
    with mock.patch('server.routes.chat_messages.send_firebase_message'):
        resp = client.post('/chat_message/test_room/', data=json.dumps({
            'text': 'test',
            'purchase_id': purchase.get_id(),
        }), content_type='application/json')

    assert resp.status_code == 200
    assert len(ChatMessage.get_many()) == 1
