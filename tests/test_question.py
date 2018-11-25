import json

from server.model.account import Account
from server.model.question import Question


def test_article_questions_initially_empty(client, article):
    resp = client.get(f'/article/{article.get_id()}/question/')
    assert resp.status_code == 200
    assert not resp.json['data']


def test_article_post_question(client, article):
    resp = client.post(f'/article/{article.get_id()}/question/',
                       data=json.dumps({
                           'question': "my question"
                       }), content_type='application/json')

    assert resp.status_code == 200
    assert len(Question.get_many()) == 1


def test_article_answer_question(client, article):
    resp = client.post(f'/article/{article.get_id()}/question/',
                       data=json.dumps({
                           'question': "my question"
                       }), content_type='application/json')

    _id = resp.json['_id']
    resp = client.post(f'/article/{article.get_id()}/question/{_id}/',
                       data=json.dumps({
                           'answer': 'my answer'
                       }), content_type='application/json')

    assert resp.status_code == 200
    assert resp.json['data']['question'] == "my question"
    assert resp.json['data']['answer'] == "my answer"


def test_post_question_bad_article_id(client):
    resp = client.post('/article/{bad_id}/question/',
                       data=json.dumps({
                           'question': 'my_question'
                       }), content_type='application/json')
    assert resp.status_code == 400


def test_post_question_invalid_id(client, article):
    bad_id = article.get_id()
    bad_id = bad_id[:-1] + 'z'
    resp = client.post(f'/article/{bad_id}/question/',
                       data=json.dumps({
                           'question': 'my_question'
                       }), content_type='application/json')
    assert resp.status_code == 400


def test_question_get_question_bad_article_id(client):
    resp = client.get('/article/bad_id/question/')
    assert resp.status_code == 400


def test_question_get_question_invalid_article_id(client, article):
    bad_id = article.get_id()
    bad_id = bad_id[:-1] + 'z'
    resp = client.get(f'/article/{bad_id}/question/')
    assert resp.status_code == 400


def test_answer_bad_article_id(client):
    resp = client.post('/article/{bad_id}/question/{bad_question_id}/',
                       data=json.dumps({
                           'question': 'my_question'
                       }), content_type='application/json')

    assert resp.status_code == 400


def test_answer_empty_body(client, article):
    resp = client.post(f'/article/{article.get_id()}/question/',
                       data=json.dumps({
                           'question': "my question"
                       }), content_type='application/json')

    _id = resp.json['_id']
    resp = client.post(f'/article/{article.get_id()}/question/{_id}/')

    assert resp.status_code == 400


def test_anwser_no_answer_in_body(client, article):
    resp = client.post(f'/article/{article.get_id()}/question/',
                       data=json.dumps({
                           'question': "my question"
                       }), content_type='application/json')

    _id = resp.json['_id']
    resp = client.post(f'/article/{article.get_id()}/question/{_id}/',
                       data=json.dumps({
                       }), content_type='application/json')

    assert resp.status_code == 400


def test_list_questions_initially_empty(client):
    resp = client.get('/question/')
    assert not resp.json['data']
    assert isinstance(resp.json['data'], list)
