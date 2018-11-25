from flask import Blueprint

from server import utils
from server.model.chat_message import ChatMessage

CHAT_MESSAGES_BP = Blueprint('chat_messages', __name__,
                             url_prefix='/chat_message')


@CHAT_MESSAGES_BP.route('/<room_id>/', methods=['GET'])
def find_all(room_id):
    return utils.find_all(ChatMessage,
                          lambda: ChatMessage.get_many(room=room_id))


@CHAT_MESSAGES_BP.route('/<room_id>/', methods=['POST'])
def create(room_id):
    return utils.create(ChatMessage, additional_fields={'room': room_id})
