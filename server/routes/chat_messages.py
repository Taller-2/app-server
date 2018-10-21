from flask import Blueprint

from server import utils
from server.model.chat_message import ChatMessage

CHAT_MESSAGES_BP = Blueprint('chat_messages', __name__,
                             url_prefix='/chat-message')


@CHAT_MESSAGES_BP.route('/', methods=['GET'])
def find_all():
    return utils.find_all(ChatMessage)


@CHAT_MESSAGES_BP.route('/', methods=['POST'])
def create():
    return utils.create(ChatMessage)
