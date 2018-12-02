from flask import Blueprint, request, jsonify

from server.controllers.question import QuestionController
from server.libs.firebase import FirebaseMessage
from server.model.account import Account
from server.model.article import Article
from server.model.question import Question
from server.utils import response, patch

QUESTIONS_BP = Blueprint('questions', __name__, url_prefix='/question')


@QUESTIONS_BP.route('/', methods=['GET'])
def get():
    try:
        questions = QuestionController(**request.args).get_questions()
    except ValueError as e:
        return response(message=f"Error parsing querystring parameters. "
                                f"{e}",
                        ok=False), 400
    except KeyError as e:
        keys = ', '.join(Question.schema.keys())
        return response(message=f"Invalid key {e}. "
                                f"Valid parameters are {keys}",
                        ok=False), 400

    return jsonify({'data': questions, 'ok': True})


@QUESTIONS_BP.route('/', methods=['PATCH'])
def patch_question():
    resp, status_code = patch(Question)
    if status_code == 200:
        question = Question.get_one(resp.json['data']['_id'])
        article = Article.get_one(question['article_id'])
        FirebaseMessage({
            'title': f'Nueva respuesta sobre {article["name"]}',
            'message': f'{question["answer"]}',
            'article_id': question['article_id'],
            'type': 'new_answer'
        }, to=Account.get_one(question['user_id'])).send()
    return resp, status_code


@QUESTIONS_BP.route("/<_id>/", methods=['GET'])
def get_one(_id):
    try:
        return jsonify(Question.get_one(_id).to_json()), 200
    except ValueError:
        return response(message=f"Question {_id} not found",
                        ok=False), 400
