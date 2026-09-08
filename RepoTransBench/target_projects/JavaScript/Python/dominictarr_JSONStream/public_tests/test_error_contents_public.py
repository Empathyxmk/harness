import pytest
from src.jsonstream import jsonstream

def test_error_contains_json_snippet():
    parser = jsonstream.parse()
    with pytest.raises(Exception) as exc_info:
        for _ in parser.parse_string('{ "wrong": }'):
            pass
    assert 'Unexpected token' in str(exc_info.value)
    assert '"wrong"' in str(exc_info.value)

def test_error_contains_partial_input():
    parser = jsonstream.parse()
    with pytest.raises(Exception) as exc_info:
        for _ in parser.parse_string('{ "foo": '):
            pass
    assert str(exc_info.value)