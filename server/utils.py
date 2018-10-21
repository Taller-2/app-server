from flask import request, jsonify


# pylint: disable=C0103
def response(message: str, ok: bool, **kwargs):
    """Arma una respuesta json generica"""
    return jsonify({'message': message, 'ok': ok, **kwargs})


def find_all(cls):
    try:
        instances = cls.get_many(**request.args)
    except ValueError:
        received = request.query_string.decode('utf-8')
        return response(message=f"Error parsing querystring parameters. "
                                f"Received '{received}'",
                        ok=False), 400
    except KeyError as e:
        keys = ', '.join(cls.schema.keys())
        return response(message=f"Invalid key {e}. "
                                f"Valid parameters are {keys}",
                        ok=False), 400
    data = [instance.to_json() for instance in instances]
    return jsonify({"ok": True, "data": data}), 200


def create(cls, optional_fields=None, additional_fields=None):
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
    return jsonify({"ok": True, "_id": _id}), 200
