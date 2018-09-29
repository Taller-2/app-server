import pytest

from server.model.base import Model
from server.libs.mongo import mongo


def setup_function():
    mongo.db['test_db'].delete_many({})


# Sample model implementation for tests
class TestModel(Model):
    schema = {
        'test_field': str
    }

    db_name = 'test_db'


def test_model_cant_delete_if_not_saved():
    with pytest.raises(AttributeError):
        TestModel({'test_field': 'hola'}).delete()


def test_model_discards_extra_fields():
    model = TestModel({'test_field': 'hola',
                       'extra_field': 'chau'})

    with pytest.raises(KeyError):
        # noinspection PyStatementEffect
        model['extra_field']


def test_set_item_outside_schema():
    model = TestModel({'test_field': 'hola'})

    with pytest.raises(KeyError):
        model['extra_field'] = "chau"


def test_update_item_in_schema():
    model = TestModel({"test_field": "hola"})

    model['test_field'] = "chau"

    assert model.to_json()['test_field'] == 'chau'


def test_get_models_initially_empty():
    models = TestModel.get_many()  # Get all
    assert len(models) == 0


def test_write_model_to_db():
    model = TestModel({"test_field": "hola"})

    model.save()

    models = TestModel.get_many()  # Get all
    assert len(models) == 1


def test_delete_model():

    model = TestModel({"test_field": "hola"})

    model.save()

    model.delete()
    assert len(TestModel.get_many()) == 0
