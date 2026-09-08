import pytest
from src.objects_to_csv import objects_to_csv

def test_public_input_not_array():
    with pytest.raises(TypeError):
        objects_to_csv(None)
    with pytest.raises(TypeError):
        objects_to_csv(0)
    with pytest.raises(TypeError):
        objects_to_csv(True)
    with pytest.raises(TypeError):
        objects_to_csv('array')

def test_public_empty_array():
    assert objects_to_csv([]) == ""

def test_public_csv_header_all_keys():
    arr = [
        {"name": "Alice", "age": 30},
        {"name": "Bob", "age": 25}
    ]
    assert objects_to_csv(arr) == '"name","age"\nAlice,30\nBob,25'

def test_public_include_all_fields():
    arr = [
        {"animal": "cat", "color": "black"},
        {"animal": "dog", "tail": True}
    ]
    assert objects_to_csv(arr) == '"animal","color","tail"\ncat,black,\ndog,,True'

def test_public_specifying_fields_option():
    arr = [{"id": 5, "a": "x", "b": "y"}]
    assert objects_to_csv(arr, {"fields": ["b", "id"]}) == '"b","id"\ny,5'

def test_public_escape_delimiter_quotes_newlines():
    arr = [
        {"description": "text,with,comma", "info": "info"},
        {"description": 'has"doublequote', "info": "multi\nline"},
        {"description": "foo", "info": "bar"}
    ]
    csv = objects_to_csv(arr, {"fields": ["description", "info"]})
    assert csv == '"description","info"\n"text,with,comma",info\n"has""doublequote","multi\nline"\nfoo,bar'

def test_public_custom_delimiter():
    arr = [{"x": 100, "y": 200}]
    assert objects_to_csv(arr, {"delimiter": "|"}) == '"x"|"y"\n100|200'

def test_public_no_header_option():
    arr = [{"first": "A", "second": "B"}]
    csv = objects_to_csv(arr, {"header": False})
    assert csv == "A,B"

def test_public_null_and_undefined_properties():
    arr = [{"foo": None, "bar": None, "baz": 42}]
    assert objects_to_csv(arr) == '"foo","bar","baz"\n,,42'