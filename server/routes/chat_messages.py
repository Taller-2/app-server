from flask import Blueprint, request

from server import utils
from server.decorators.login_required import login_required
from server.libs.firebase import FirebaseMessage
from server.model.account import Account
from server.model.chat_message import ChatMessage
from server.model.purchase import Purchase

CHAT_MESSAGES_BP = Blueprint('chat_messages', __name__,
                             url_prefix='/chat_message')


@CHAT_MESSAGES_BP.route('/<room_id>/', methods=['GET'])
def find_all(room_id):
    return utils.find_all(ChatMessage,
                          lambda: ChatMessage.get_many(room=room_id))


@CHAT_MESSAGES_BP.route('/<room_id>/', methods=['POST'])
@login_required
def create(room_id):
    purchase_id = request.get_json(silent=True).get('purchase_id')
    account = Account.current()
    response, status_code = \
        utils.create(ChatMessage,
                     additional_fields={'room': room_id,
                                        'name': account['name'],
                                        'sender_user_id': account.get_id()})

    if status_code == 200 and purchase_id is not None:
        send_firebase_message(response.json['_id'], purchase_id)
    return response, status_code


def send_firebase_message(message_id, purchase_id):
    # ☢️☢️☢️☢️☢️
    # Sends a firebase message, to the inferred recipient
    message = ChatMessage.get_one(message_id)

    sender_id = message['sender_user_id']
    purchase = Purchase.get_one(purchase_id)
    seller = purchase.seller()
    buyer = Account.get_one(purchase['user_id'])
    if sender_id == seller.get_id():
        sender = seller
        recipient = buyer
    else:
        sender = buyer
        recipient = seller
    FirebaseMessage(message_data={
        'title': sender['name'],
        'message': message['text'],
        'purchase_id': purchase_id},
                    to=recipient).send()
