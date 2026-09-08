import pytest
import sys
import types

from forms_builder.forms import fields

def test_linebreak_re():
    assert fields.linebreak_re.split("a\nb") == ['a', 'b']
    assert fields.linebreak_re.split("a\r\nb") == ['a', 'b']
    assert fields.linebreak_re.split("a\r\nb\nc") == ['a', 'b', 'c']

def test_field_type_iterable():
    # There should be at least 1 type, and it's a tuple of 2
    types_list = fields.FIELD_TYPES
    assert isinstance(types_list, (list, tuple))
    for t in types_list:
        assert isinstance(t, tuple) and len(t) == 2

def test_choices_from_lines_basic():
    choices = "Red\nGreen\nBlue"
    expected = [("Red", "Red"), ("Green", "Green"), ("Blue", "Blue")]
    assert fields.choices_from_lines(choices) == expected

def test_choices_from_lines_empty():
    assert fields.choices_from_lines("") == []
    assert fields.choices_from_lines(None) == []
    assert fields.choices_from_lines(1) == []
    # Handles basic list/tuple pass-through
    out = fields.choices_from_lines([("foo", "foo")])
    assert out == [("foo", "foo")]