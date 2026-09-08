import pytest
from src import postal

def test_expand_not_throw_numeric_input():
    try:
        postal.expand(12345)
    except Exception:
        pytest.fail("postal.expand should not throw on numeric input.")

def test_expand_not_throw_on_null_input():
    try:
        postal.expand(None, None)
    except Exception:
        pytest.fail("postal.expand should not throw on null inputs.")

def test_expand_return_array_weird_options():
    options = {"languages": None, "address_country": 42}
    result = postal.expand('weird', options)
    assert isinstance(result, list)

def test_parser_not_throw_on_number():
    try:
        postal.parser(98765)
    except Exception:
        pytest.fail("postal.parser should not throw on number input.")

def test_parser_not_throw_on_object():
    try:
        postal.parser({"foo": "bar"})
    except Exception:
        pytest.fail("postal.parser should not throw on object input.")