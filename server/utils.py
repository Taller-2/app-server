import os
from datetime import datetime, timedelta
from typing import Callable, Sequence, Type

import jwt
from flask import request, jsonify, current_app

from server.model.base import Model


# pylint: disable=C0103
def response(message: str, ok: bool, **kwargs):
    """Arma una respuesta json generica"""
    return jsonify({'message': message, 'ok': ok, **kwargs})


def find_all(cls: Type[Model],
             get_instances: Callable[[], Sequence[Model]] = None):
    try:
        if get_instances:
            instances = get_instances()
        else:
            instances = cls.get_many(**request.args)
    except ValueError as e:
        return response(message=f"Error parsing querystring parameters. "
                                f"{e}",
                        ok=False), 400
    except KeyError as e:
        keys = ', '.join(cls.schema.keys())
        return response(message=f"Invalid key {e}. "
                                f"Valid parameters are {keys}",
                        ok=False), 400
    data = [instance.to_json() for instance in instances]
    return jsonify({"ok": True, "data": data}), 200


def create(cls: Type[Model],
           optional_fields: Sequence[str] = None,
           additional_fields: dict = None,
           after_save=None):
    body = request.get_json(silent=True)

    if not body:
        return response("Invalid or empty request body", ok=False), 400

    if additional_fields:
        body.update(additional_fields)

    # Optional fields, zero or more. If not present, init them as an empty list
    if optional_fields:
        for field in optional_fields:
            body.setdefault(field, [])

    try:
        instance = cls(body)
    except ValueError as e:
        return response(message=f"Error in validation: {e}", ok=False), 400

    _id = instance.save()
    if after_save:
        after_save(instance)
    return jsonify({"ok": True, "_id": _id}), 200


def get_shared_server_auth_header():
    if current_app.config['SKIP_AUTH']:
        return {'X-Auth-App': 'a mock'}
    encoded = jwt.encode(
        {
            'name': os.environ.get('APP_SERVER_NAME'),
            'exp': datetime.utcnow() + timedelta(minutes=1)
        },
        os.environ.get('APP_SERVER_SECRET'),
        algorithm='HS256'
    )
    return {'X-Auth-App': encoded}


def patch(model: Type[Model]):
    body = request.get_json(silent=True)
    if not body:
        return response("Invalid or empty request body", ok=False), 400
    _id = body.get('_id')
    if _id is None:
        return response("_id field invalid", ok=False), 400
    try:
        instance = model.get_one(_id)
    except ValueError:
        return response(f'Bad article id: {_id}', ok=False), 400
    try:
        instance.update(**body)
    except ValueError as e:
        return response(message=f"Error in validation: {e}", ok=False), 400
    return jsonify({"ok": True, "data": instance.to_json()}), 200
