import pytest
from forms_builder.forms import fields

def test_public_field_to_python_boolean_true():
    boolean_field = fields.FIELD_MAP["boolean"]()
    assert boolean_field.to_python("on") is True

def test_public_field_to_python_boolean_false():
    boolean_field = fields.FIELD_MAP["boolean"]()
    assert boolean_field.to_python("") is False
    assert boolean_field.to_python(None) is False

def test_public_field_to_python_select():
    select_field = fields.FIELD_MAP["select"](choices="orange|banana|pear")
    assert select_field.choices == ["orange", "banana", "pear"]

def test_public_pretty_name_with_number():
    assert fields.pretty_name("item_123_value") == "Item 123 value"