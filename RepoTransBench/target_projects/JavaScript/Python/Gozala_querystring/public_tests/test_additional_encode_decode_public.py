import pytest
from gozala_querystring.encode import encode
from gozala_querystring.decode import decode

def test_encode_object_with_different_url_special_characters_public():
    result1 = encode({'search': "baz qux", 'weird': "^~,"})
    assert result1 == "search=baz%20qux&weird=%5E~%2C"
    result2 = encode({'path': "foo/bar", 'percent': "%", 'plus': "+"})
    assert result2 == "path=foo%2Fbar&percent=%25&plus=%2B"

def test_encode_empty_object_as_empty_string_public():
    result = encode({})
    assert result == ""

def test_encode_numeric_keys_and_values_public():
    result = encode({120: 555, 88: 1234})
    possible = ["120=555&88=1234", "88=1234&120=555"]
    assert result in possible

def test_encode_null_and_undefined_as_empty_public():
    result = encode({'foo': None, 'bar': None, 'xyz': 'z'})
    parts = sorted(result.split('&'))
    assert parts == sorted(['foo=', 'bar=', 'xyz=z'])

def test_encode_multiple_types_public():
    # Arrays produce repeating keys; arr can be any order
    result = encode({'bool': True, 'arr': [7, "m"], 'str': "zxy"})
    options = [
        "bool=true&arr=7&arr=m&str=zxy",
        "bool=true&arr=m&arr=7&str=zxy",
        "arr=7&arr=m&bool=true&str=zxy",
        "arr=m&arr=7&bool=true&str=zxy",
        "str=zxy&bool=true&arr=7&arr=m",
        "str=zxy&bool=true&arr=m&arr=7"
    ]
    assert result in options

def test_decode_string_to_object_public():
    result = decode("lat=42&lon=73")
    assert result == {'lat': "42", 'lon': "73"}

def test_decode_percent_encoded_values_public():
    result = decode("greeting=hi%21")
    assert result == {'greeting': "hi!"}

def test_decode_multiple_with_same_key_public():
    result = decode("value=a&value=b&value=c")
    assert result == {'value': ["a", "b", "c"]}

def test_decode_empty_string_as_empty_object_public():
    result = decode("")
    assert result == {}

def test_decode_null_and_missing_values_as_empty_string_public():
    obj = decode("empty&set=")
    assert obj == {'empty': '', 'set': ''}

def test_decode_encoded_reserved_chars_public():
    result = decode("symbols=%24%40%5E")
    assert result == {'symbols': "$@^"}