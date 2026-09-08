import pytest
from forms_builder.forms import fields

def test_public_split_choices_diff_input():
    # Use a different string and delimiter for public test
    value = "red|green|blue"
    choices = fields.split_choices(value, "|")
    assert choices == ["red", "green", "blue"]

def test_public_pretty_name_diff_input():
    val = "zip_code"
    assert fields.pretty_name(val) == "Zip code"

def test_public_is_empty_diff_input():
    # Test with None (should be true)
    assert fields.is_empty(None)
    # Test with list containing a non-empty value (should be false)
    assert not fields.is_empty(["value"])
    # Test with string containing only whitespace (should be true)
    assert fields.is_empty("      ")