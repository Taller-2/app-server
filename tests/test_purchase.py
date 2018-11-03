import json


def test_get_user_purchases(client):
    resp = client.get('/purchase/')
    assert resp.status_code == 200
    assert not resp.json['data']


def test_post_purchase(client, article):
    resp = client.post('/purchase/', data=json.dumps({
        "article_id": article.get_id(),
        "units": article['available_units']
    }), content_type='application/json')

    assert resp.status_code == 200

    resp = client.get('/purchase/')
    assert resp.status_code == 200
    article = article.to_json()
    resp_article = resp.json['data'][0]['article']
    for key in article:
        assert resp_article[key] == article[key]


def test_post_bad_article(client):
    resp = client.post('/purchase/', data=json.dumps({
        "units": 1,
    }), content_type='application/json')

    assert resp.status_code == 400
