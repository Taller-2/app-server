from flask import jsonify


# pylint: disable=C0103
def response(message: str, ok: bool, **kwargs):
    """Arma una respuesta json generica"""
    return jsonify({'message': message, 'ok': ok, **kwargs})


def validate_mongo_object_id(_id: str) -> bool:
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
