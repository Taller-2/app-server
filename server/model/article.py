import typing
from typing import Optional, Union


class Article:
    SCHEMA = {
        'name': str,
        'description': str,
        'available_units': int,
        'price': Union[int, float],
        'user': str,
        'latitude': Union[int, float],
        'longitude': Union[int, float],
        'pictures': Optional[list],
        'payment_methods': Optional[list],
        'tags': Optional[list]
    }

    def __init__(self, json: dict = None, _id: str = None):
        if json is not None:
            self.validate(json)
            self._data = json.copy()

    def __getitem__(self, item):
        return self._data.get(item)

    @classmethod
    def validate(cls, json):
        for field, expected_type in cls.SCHEMA.items():
            value = json.get(field)
            if type(expected_type) == typing._Union:  # Hacks
                valid_type = False
                for _type in expected_type.__args__:
                    if isinstance(value, _type):
                        valid_type = True

                if not valid_type:
                    throw_bad_type_union(field, expected_type, type(value))
            else:
                if not isinstance(value, expected_type):
                    throw_bad_type(field, expected_type, type(value))


def throw_bad_type_union(field, union, got_type):
    types = "or ".join([t.__name__ for t in union.__args__])
    raise ValueError(f"Bad type for field {field}. "
                     f"Expected {types}, "
                     f"got {got_type.__name__}")


def throw_bad_type(field, expected_type, got_type):
    type_name = \
        got_type.__name__ if got_type is type(None) else "null"  # noqa: E721

    raise ValueError(f"Bad type for field '{field}'. "
                     f"Expected {expected_type.__name__}, "
                     f"got {type_name}")
