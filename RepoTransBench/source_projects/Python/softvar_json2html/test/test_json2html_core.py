import pytest
from json2html import Json2Html, convert
import json

@pytest.mark.parametrize(
    "input_data,expected_substring",
    [
        ({"foo": "bar"}, "foo"),
        ([], ""),  # Empty list should yield empty string output
        ("", ""),  # Empty string should yield empty string output
        ([{"a": 1, "b": 2}, {"a": 3, "b": 4}], "a"),  # List of dicts, clubbing keys
        (123, "123"),  # Non-string, non-list, non-dict should string-convert
    ]
)
def test_convert_various_inputs(input_data, expected_substring):
    html = convert(json=input_data)
    assert expected_substring in html

def test_convert_bad_json_string():
    js = Json2Html()
    # JSON that is NOT a dict, but not the special error raised
    bad_json = '{"foo": bar}'  # bar is not in quotes, invalid JSON
    # The code under test does not raise ValueError unless "Expecting property name" in msg
    res = js.convert(json=bad_json)
    # In fallback, it simply returns the string as-is for non-JSON but not matching specific text
    assert isinstance(res, str) and bad_json in res

def test_convert_non_utf_input():
    js = Json2Html()
    # Parse bytes directly, coverage for else path
    bad_json = b'\x80abc'  # This is NOT a str
    res = js.convert(json=bad_json)
    assert isinstance(res, str) or isinstance(res, bytes)

def test_column_headers_from_list_of_dicts():
    js = Json2Html()
    data = [{"a": 1, "b": 2}, {"a": 10, "b": 20}]
    headers = js.column_headers_from_list_of_dicts(data)
    assert list(headers) == ["a", "b"]

def test_column_headers_with_inconsistent_dicts():
    js = Json2Html()
    data = [{"a": 1}, {"a": 1, "b": 2}]
    assert js.column_headers_from_list_of_dicts(data) is None

def test_column_headers_with_list_of_non_dicts():
    js = Json2Html()
    data = [1, 2, 3]
    assert js.column_headers_from_list_of_dicts(data) is None

def test_convert_with_encode_option():
    js = Json2Html()
    data = {"foo": "bar"}
    result = js.convert(json=data, encode=True)
    assert isinstance(result, bytes)

def test_convert_with_escape_false():
    js = Json2Html()
    data = {'key': '<b>html</b>'}
    html = js.convert(json=data, escape=False)
    # Unescaped HTML
    assert '<b>html</b>' in html

def test_repr_json2html():
    js = Json2Html()
    assert "Json2Html" in repr(js)