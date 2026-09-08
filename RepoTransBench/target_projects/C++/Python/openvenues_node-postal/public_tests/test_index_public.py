import pytest
from src import postal

def test_expand_on_different_normal_string_address():
    res = postal.expand('456 Elm St, New York', {'languages': ['fr']})
    assert isinstance(res, list)

def test_expand_not_throw_on_whitespace_string():
    try:
        postal.expand('   ')
    except Exception:
        pytest.fail("postal.expand should not throw on whitespace string.")

def test_expand_return_array_with_options_null_undefined():
    res = postal.expand('example', {'languages': None, 'lowercase': None})
    assert isinstance(res, list)

def test_parser_return_array_for_different_string_address():
    parsed = postal.parser('999 Unknown Rd, Imagineland')
    assert isinstance(parsed, list)

def test_parser_not_throw_on_missing_options_another_address():
    try:
        postal.parser('55 Example Blvd, Gotham')
    except Exception:
        pytest.fail("postal.parser should not throw on missing options for another address.")