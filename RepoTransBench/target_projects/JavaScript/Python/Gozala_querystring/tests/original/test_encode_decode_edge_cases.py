import pytest
from gozala_querystring.encode import encode
from gozala_querystring.decode import decode

def test_encode_object_with_undefined_value_as_empty_string():
    result = encode({'a': None, 'b': 2})
    assert result == "a=&b=2"

def test_encode_arrays_in_object():
    result = encode({'a': [1, 2, 3], 'b': "ok"})
    assert result == "a=1&a=2&a=3&b=ok"

def test_encode_array_of_arrays_as_empty_string_for_each_element():
    result = encode({'arr': [[1, 2], [3, 4]]})
    assert result == "arr=&arr="

def test_encode_object_with_functions_value_becomes_empty():
    def dummy_func():
        pass
    s = encode({'a': "str", 'func': dummy_func, 'b': True})
    assert "a=str" in s
    assert "b=true" in s
    assert "func=" in s

def test_encode_null_and_boolean_values_with_null_as_empty_string():
    result = encode({'a': None, 'b': False, 'c': 0})
    assert result == "a=&b=false&c=0"

def test_decode_to_object_with_multiple_keys():
    result = decode("a=1&b=2&c=3")
    assert result == {'a': "1", 'b': "2", 'c': "3"}

def test_decode_repeated_keys_as_array():
    result = decode("a=1&a=2&a=3")
    assert result == {'a': ["1", "2", "3"]}

def test_decode_empty_value():
    result = decode("a=&b=2")
    assert result == {'a': "", 'b': "2"}

def test_decode_array_encoded_and_uri_components():
    result = decode("arr=1%2C2&arr=3%2C4")
    assert result == {'arr': ["1,2", "3,4"]}

def test_decode_plus_as_space():
    result = decode("a=hello+world&b=1+2")
    assert result == {'a': "hello world", 'b': "1 2"}

def test_decode_null_false_true_string_values_as_they_are():
    result = decode("a=null&b=false&c=true")
    assert result == {'a': "null", 'b': "false", 'c': "true"}