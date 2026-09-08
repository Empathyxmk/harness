import pytest
from benface_tailwindcss_transforms.prefix_negative_modifiers import prefix_negative_modifiers

def test_is_defined_if_exported():
    assert callable(prefix_negative_modifiers)

def test_returns_object_unchanged_when_values_are_not_numbers_strings():
    out = prefix_negative_modifiers({'foo': True, 'bar': None})
    assert out == {'foo': True, 'bar': None}

def test_adds_prefix_to_negative_number_values():
    out = prefix_negative_modifiers({'a': -1, 'b': 2})
    assert out == {'a': "-1", 'b': "2"}

def test_adds_prefix_to_negative_string_numbers():
    out = prefix_negative_modifiers({'a': "-5", 'b': "1"})
    assert out == {'a': "-5", 'b': "1"}

def test_handles_empty_object():
    assert prefix_negative_modifiers({}) == {}

def test_handles_zero_and_strings_with_minus():
    # In JS, -0 to "0"
    out = prefix_negative_modifiers({'a': 0, 'b': "-0", 'c': -0})
    assert out == {'a': "0", 'b': "-0", 'c': "0"}