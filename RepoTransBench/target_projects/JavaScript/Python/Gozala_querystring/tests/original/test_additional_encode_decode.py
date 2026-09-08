import pytest
from gozala_querystring.encode import encode
from gozala_querystring.decode import decode

def test_encode_simple_object():
    result = encode({'foo': "bar", 'baz': 1})
    assert result == "foo=bar&baz=1"

def test_encode_with_special_url_characters():
    result = encode({'q': "hello world", 'sym': "&=?"})
    assert result == "q=hello%20world&sym=%26%3D%3F"

def test_encode_empty_object_as_empty_string():
    result = encode({})
    assert result == ""

def test_decode_single_pair():
    result = decode("a=1")
    assert result == {'a': "1"}

def test_decode_empty_string_as_empty_object():
    result = decode("")
    assert result == {}

def test_decode_keys_with_encoded_characters():
    result = decode("q=hello%20world&sym=%26%3D%3F")
    assert result == {'q': "hello world", 'sym': "&=?"}

def test_decode_equals_with_missing_value_as_empty_string():
    result = decode("a=&b=")
    assert result == {'a': "", 'b': ""}