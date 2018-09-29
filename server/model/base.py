import typing
from bson import ObjectId

from server.libs.mongo import mongo


class Model:
    # Schema to validate the documents against. Keys: field names
    # values: types to validate against (use Python's typing module)
    schema = {}

    # Mongodb database name. Try to keep this unique between models!
    db_name = None

    def __init__(self, json: dict):
        self.validate(json)
        self._data = json.copy()
        for key in filter(lambda x: x not in self.valid_keys(),
                          list(json.keys())):
            json.pop(key)

        self._id = None

    def __getitem__(self, item):
        self.validate_key_in_schema(item)

        return self._data.get(item)

    def __setitem__(self, field, value):
        self.validate_key_in_schema(field)

        expected_type = self.schema[field]
        validate_type(field, value, expected_type)

        self._data[field] = value

    def validate_key_in_schema(self, field):
        if field not in self.schema.keys():
            name = self.__class__.__name__
            raise KeyError(f"{field} is not a valid attribute of {name}")

    @classmethod
    def validate(cls, json):
        for field, expected_type in cls.schema.items():
            value = json.get(field)
            validate_type(field, value, expected_type)

    @classmethod
    def get_one(cls, _id):
        doc = mongo.db[cls.db_name].find_one({'_id': ObjectId(_id)})
        if doc:
            model = cls(doc)
            model._id = doc['_id']
            return model

        return None

    def delete(self):
        if not self._id:
            name = self.__class__.__name__
            raise AttributeError(f"{name} instance is not loaded in db")

        return mongo.db[self.db_name].delete_one({'_id': self._id})

    @classmethod
    def get_many(cls, *_, **kwargs):
        models = []
        results = mongo.db[cls.db_name].find(kwargs)

        for result in results:
            model = cls(result)
            model._id = result['_id']
            models.append(model)

        return models

    def to_json(self):
        data = self._data.copy()
        data.update({'_id': self._id})
        return data

    def save(self):
        result = mongo.db[self.db_name].insert_one(self._data)
        self._id = result.inserted_id
        return str(result.inserted_id)

    def valid_keys(self):
        return list(self.schema) + ['_id']


def throw_bad_type_union(field, union, got_type):
    types = " or ".join([t.__name__ for t in union.__args__])
    raise ValueError(f"Bad type for field {field}. "
                     f"Expected {types}, "
                     f"got {got_type.__name__}")


def throw_bad_type(field, expected_type, got_type):
    type_name = \
        got_type.__name__ if got_type is not type(None) else "null"  # noqa: E721

    raise ValueError(f"Bad type for field '{field}'. "
                     f"Expected {expected_type.__name__}, "
                     f"got {type_name}")


def validate_type(field_name: str, value: typing.Any, expected_type):
    if type(expected_type) == typing._Union:  # Hacks
        valid_type = False
        for _type in expected_type.__args__:
            if isinstance(value, _type):
                valid_type = True

        if not valid_type:
            throw_bad_type_union(field_name, expected_type, type(value))
    else:
        if not isinstance(value, expected_type):
            throw_bad_type(field_name, expected_type, type(value))
