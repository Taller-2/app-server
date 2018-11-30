from server.logger.logger import get_root_logger

import firebase_admin
from firebase_admin import credentials, messaging
from flask import current_app

from server.model.account import Account

API_KEY_PATH = "apikey.json"

logger = get_root_logger("Firebase")


class FirebaseMessage:
    def __init__(self, title: str, message: str, to: Account):
        self.title = title
        self.message = message
        self.recipient = to

    def send(self):
        if not self.is_firebase_initialized():
            self.init_firebase()

        registration_token = self.recipient['instance_id']
        if registration_token is None:
            msg = "Account instance id is None, skipping firebase message. " \
                  "User %s"
            logger.info(msg, self.recipient.get_id())
            return

        # See documentation on defining a message payload.
        firebase_message = messaging.Message(
            data={
                'title': self.title,
                'message': self.message,
            },
            token=registration_token,
        )
        logger.info("Sending Firebase message: "
                    "title: %s, message %s, token %s",
                    self.title, self.message, registration_token)

        messaging.send(firebase_message)

    @staticmethod
    def init_firebase():
        api_key = current_app.config['FIREBASE_API_KEY']
        logger.info("Initializing Firebase client. API KEY: %s", api_key)
        with open(API_KEY_PATH, mode='w') as f:
            f.write(api_key)

        cred = credentials.Certificate(API_KEY_PATH)
        firebase_admin.initialize_app(cred)

    @staticmethod
    def is_firebase_initialized():
        try:
            firebase_admin.get_app()
            return True
        except ValueError:
            return False
