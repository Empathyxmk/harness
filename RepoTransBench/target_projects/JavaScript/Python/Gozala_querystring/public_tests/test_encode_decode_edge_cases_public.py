import pytest
from gozala_querystring.encode import encode
from gozala_querystring.decode import decode

def test_encode_object_with_undefined_value_as_empty_string_public():
    result = encode({'x': None, 'y': 42})
    assert result == "x=&y=42"

def test_encode_arrays_in_object_public():
    result = encode({'fruits': ['apple', 'banana', 'cherry'], 'count': 3})
    assert result == "fruits=apple&fruits=banana&fruits=cherry&count=3"

def test_encode_array_of_arrays_as_empty_string_for_each_element_public():
    result = encode({'arr': [[5, 6], [7, 8]]})
    assert result == "arr=&arr="

def test_encode_object_with_functions_value_becomes_empty_public():
    def my_func():
        pass
    s = encode({'hello': "world", 'myFunc': my_func, 'flag': False})
    assert "hello=world" in s
    assert "flag=false" in s
    assert "myFunc=" in s

def test_encode_null_and_boolean_values_with_null_as_empty_string_public():
    result = encode({'a': None, 'b': True, 'c': -1})
    assert result == "a=&b=true&c=-1"

def test_decode_to_object_with_multiple_keys_public():
    result = decode("x=42&y=0&z=NaN")
    assert result == {'x': "42", 'y': "0", 'z': "NaN"}

def test_decode_repeated_keys_as_array_public():
    result = decode("val=a&val=b&val=c")
    assert result == {'val': ["a", "b", "c"]}

def test_decode_empty_value_public():
    result = decode("x=&y=100")
    assert result == {'x': "", 'y': "100"}

def test_decode_array_encoded_and_uri_components_public():
    result = decode("list=apple%2Cpie&list=banana%2Csplit")
    assert result == {'list': ["apple,pie", "banana,split"]}

def test_decode_plus_as_space_public():
    result = decode("x=foo+bar&y=1+1")
    assert result == {'x': "foo bar", 'y': "1 1"}

def test_decode_null_false_true_string_values_as_they_are_public():
    result = decode("x=nil&y=no&z=yes")
    assert result == {'x': "nil", 'y': "no", 'z': "yes"}