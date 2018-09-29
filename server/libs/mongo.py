import datetime
import json

from bson.objectid import ObjectId
from flask_pymongo import PyMongo

mongo = PyMongo()


class JSONEncoder(json.JSONEncoder):
    # extend json encoder for compatibility with mongoDB
    def default(self, o):  # pylint: disable=E0202
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, datetime.datetime):
            return str(o)
        return json.JSONEncoder.default(self, o)


def validate_object_id(_id: str) -> bool:
    # https://docs.mongodb.com/manual/reference/method/ObjectId/#ObjectId
    # 12 byte object id == 24 byte hex string
    if not isinstance(_id, str):
        return False
    if len(_id) != 24:
        return False

    try:
        int(_id, base=16)
    except ValueError:
        return False

    return True
