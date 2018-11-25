from flask import Blueprint

from server.model.question import Question
from server.utils import find_all

QUESTIONS_BP = Blueprint('questions', __name__, url_prefix='/question')


@QUESTIONS_BP.route('/', methods=['GET'])
def get():
    return find_all(
        Question,
    )
