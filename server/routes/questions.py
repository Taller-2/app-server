from flask import Blueprint, request, jsonify

from server.controllers.question import QuestionController
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
    return patch(Question)
