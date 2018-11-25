from server.model.base import Model


class ChatMessage(Model):
    db_name = 'chat_message'

    schema = {
        'room': str,
        'text': str,
        'name': str,
        'sender_user_id': str
    }
