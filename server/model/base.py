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
        validate_mongo_object_id(_id)
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
    def get_many(cls, *_, **kwargs) -> list:
        mongo_query = cls.make_mongo_query(kwargs)

        return cls.run_query(mongo_query)

    @classmethod
    def run_query(cls, mongo_query):
        models = []
        results = mongo.db[cls.db_name].find(mongo_query)
        for result in results:
            model = cls(result)
            model._id = result['_id']
            models.append(model)
        return models

    @classmethod
    def make_mongo_query(cls, filters: dict) -> dict:
        """

        Generates an AND of several ORs of the params given by the
        filters dict
        filters schema: {
            "param1": ["value1", "value2", ...]
            "param2": ["value3", ...]
        }
        """
        ands = []
        for key in filters:
            key_or = []
            if isinstance(filters[key], str):
                filters[key] = [filters[key]]

            for value in filters[key]:
                try:
                    value = cls.cast_value(value, key)
                except ValueError as e:
                    raise ValueError(f'Error in query parameter {key}: {e}')
                key_or.append({key: value})

            if key_or:
                ands.append({"$or": key_or})
        return {"$and": ands} if ands else {}

    def to_json(self):
        data = self._data.copy()
        data.update({'_id': self._id})
        return data

    def save(self):
        collection = mongo.db[self.db_name]
        if self._id:
            collection.update_one({'_id': self._id}, {"$set": self._data})
        else:
            self._id = collection.insert_one(self._data).inserted_id
        return str(self._id)

    def valid_keys(self):
        return list(self.schema) + ['_id']

    def update(self, **values):
        if values.get('_id'):
            values.pop('_id')

        for key in values:
            self[key] = values[key]

        return self.save()

    def get_id(self):
        return str(self._id)

    @classmethod
    def cast_value(cls, value, key):
        cast_type = cls.schema[key]

        if type(cast_type) == typing._Union:
            # Special case: if arg is a list, we return element as-is
            # we assume lists are made up of strings only
            if list in cast_type.__args__:
                return value

            for _type in cast_type.__args__:
                try:
                    return _type(value)
                except TypeError:
                    continue
            raise ValueError(f"Bad type for {value}")

        return cast_type(value)


def throw_bad_type_union(field, union, got_type):
    types = " or ".join([t.__name__ for t in union.__args__])
    raise ValueError(f"Bad type for field {field}. "
                     f"Expected {types}, "
                     f"got {got_type.__name__}")


def throw_bad_type(field, expected_type, got_type):
    type_name = got_type.__name__ \
            if got_type is not type(None) else "null"  # noqa: E721

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
            # Special case
            if expected_type == float and isinstance(value, int):
                return
            throw_bad_type(field_name, expected_type, type(value))


def throw_bad_id(_id: str):
    raise ValueError(f'{_id} is not a valid Model ID. '
                     f'It must be a 24 byte hexadecimal string')


def validate_mongo_object_id(_id: str):
    # https://docs.mongodb.com/manual/reference/method/ObjectId/#ObjectId
    # 12 byte object id == 24 byte hex string
    if not isinstance(_id, str):
        throw_bad_id(_id)
    if len(_id) != 24:
        throw_bad_id(_id)

    try:
        int(_id, base=16)
    except ValueError:
        throw_bad_id(_id)
