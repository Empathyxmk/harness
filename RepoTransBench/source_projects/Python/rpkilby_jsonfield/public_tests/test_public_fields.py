import pytest
from src.jsonfield.fields import JSONField

class DummyModel:
    # Dummy model for testing
    pass

def test_deconstruct_non_default_kwargs():
    f = JSONField(encoder_class=str, decoder_class=str, dump_kwargs={'indent': 4})
    name, path, args, kwargs = f.deconstruct()
    assert kwargs['encoder_class'] == str
    assert kwargs['decoder_class'] == str
    assert kwargs['dump_kwargs'] == {'indent': 4}

def test_deconstruct_default_kwargs():
    f = JSONField()
    name, path, args, kwargs = f.deconstruct()
    assert 'decoder_class' not in kwargs
    assert 'encoder_class' not in kwargs
    assert 'dump_kwargs' not in kwargs

def test_get_prep_value_can_return_none_if_null():
    field = JSONField(null=True)
    val = field.get_prep_value(None)
    assert val is None

def test_get_prep_value_always_json_dumps_if_not_null():
    field = JSONField(null=True)
    # Use input object with different values
    val = field.get_prep_value({"number": 33, "flag": False})
    assert val == '{"number": 33, "flag": false}'

def test_from_db_value_loaded_types():
    field = JSONField()
    assert field.from_db_value('{"z":1}', None, None, None) == {"z": 1}
    assert field.from_db_value(None, None, None, None) is None