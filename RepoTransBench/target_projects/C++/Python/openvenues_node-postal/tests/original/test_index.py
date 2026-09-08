import pytest
from src import postal

def test_expand_normal_address():
    result = postal.expand('123 Main St')
    assert isinstance(result, list)
    assert len(result) == 1
    assert '123 Main St' in result[0]

def test_expand_empty_string_address():
    result = postal.expand('')
    assert isinstance(result, list)
    assert len(result) == 1
    assert '' in result[0]

def test_expand_respect_options_argument():
    result = postal.expand('456 Elm St', {'languages': ['en']})
    assert isinstance(result, list)
    assert '456 Elm St' in result[0]

def test_expand_not_fail_if_options_omitted():
    result = postal.expand('789 Oak Ave')
    assert isinstance(result, list)

def test_expand_handle_undefined_address():
    result = postal.expand(None)
    assert isinstance(result, list)

def test_parser_normal_address():
    result = postal.parser('123 Main St')
    assert isinstance(result, list)
    assert result[0]['component'] == "road"
    assert result[0]['value'] == '123 Main St'

def test_parser_handle_empty_string():
    result = postal.parser('')
    assert isinstance(result, list)
    assert result[0]['value'] == ''

def test_parser_handle_undefined():
    result = postal.parser(None)
    assert isinstance(result, list)
    assert result[0]['value'] is None