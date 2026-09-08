import pytest
from src.objects_to_csv import objects_to_csv

def test_input_not_array():
    with pytest.raises(TypeError):
        objects_to_csv(None)
    with pytest.raises(TypeError):
        objects_to_csv({})
    with pytest.raises(TypeError):
        objects_to_csv("str")
    with pytest.raises(TypeError):
        objects_to_csv(123)

def test_empty_array():
    assert objects_to_csv([]) == ""

def test_generate_csv_with_header_and_all_keys():
    arr = [
        {"a": 1, "b": 2},
        {"a": 3, "b": 4}
    ]
    assert objects_to_csv(arr) == '"a","b"\n1,2\n3,4'

def test_include_all_fields_found_in_any_object():
    arr = [
        {"a": 1, "b": 2},
        {"a": 3, "c": 5}
    ]
    assert objects_to_csv(arr) == '"a","b","c"\n1,2,\n3,,5'

def test_specifying_fields_option():
    arr = [{"x": 1, "y": 2, "z": 3}]
    assert objects_to_csv(arr, {"fields": ["z", "x"]}) == '"z","x"\n3,1'

def test_escape_delimiter_quotes_newlines():
    arr = [
        {"text": "val,1", "text2": "plain"},
        {"text": 'with"quote', "text2": "new\nline"},
        {"text": "reg", "text2": "norm"}
    ]
    csv = objects_to_csv(arr, {"fields": ["text", "text2"]})
    assert csv == '"text","text2"\n"val,1",plain\n"with""quote","new\nline"\nreg,norm'

def test_custom_delimiter():
    arr = [{"a": 1, "b": 2}]
    assert objects_to_csv(arr, {"delimiter": ";"}) == '"a";"b"\n1;2'

def test_no_header_option():
    arr = [{"one": 1, "two": 2}]
    csv = objects_to_csv(arr, {"header": False})
    assert csv == "1,2"

def test_null_and_undefined_properties():
    arr = [{"a": None, "b": None, "c": 7}]
    assert objects_to_csv(arr) == '"a","b","c"\n,,7'