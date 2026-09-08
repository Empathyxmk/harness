import pytest

import forms_builder.forms.fields as fields


def test_split_choices_string():
    s = "Red\nBlue\r\nGreen"
    result = fields.split_choices(s)
    assert result == [("Red", "Red"), ("Blue", "Blue"), ("Green", "Green")]


def test_split_choices_empty():
    assert fields.split_choices("") == []
    assert fields.split_choices(None) == []
    assert fields.split_choices(0) == []
    assert fields.split_choices(3.14) == []


def test_split_choices_list_of_tuples():
    lst = [("A", "Apple"), ("B", "Banana")]
    assert fields.split_choices(lst) == lst


def test_split_choices_tuple_of_tuples():
    tpl = (("A", "Apple"), ("B", "Banana"))
    assert fields.split_choices(tpl) == tpl


def test_split_choices_leading_trailing_whitespace():
    s = " Red \n\n Blue"
    result = fields.split_choices(s)
    assert result == [("Red", "Red"), ("Blue", "Blue")]


def test_alias_choices_from_lines():
    s = "One\nTwo"
    result = fields.choices_from_lines(s)
    assert result == [("One", "One"), ("Two", "Two")]


def test_field_choices_and_types():
    assert isinstance(fields.FIELD_CHOICES, tuple)
    assert isinstance(fields.FIELD_TYPES, tuple)
    assert all(isinstance(i, tuple) for i in fields.FIELD_TYPES)
    assert fields.FIELD_TYPES == tuple((k, v) for k, v in fields.FIELD_CHOICES)