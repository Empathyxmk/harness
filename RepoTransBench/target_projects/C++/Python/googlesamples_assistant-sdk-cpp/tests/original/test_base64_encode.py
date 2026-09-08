import pytest
from src.assistant.base64_encode import base64_encode

def test_simple_string():
    # Equivalent to: "HelloWorld" => "SGVsbG9Xb3JsZA=="
    input_str = "HelloWorld"
    expected = "SGVsbG9Xb3JsZA=="
    assert base64_encode(input_str) == expected

def test_empty_string():
    input_str = ""
    expected = ""
    assert base64_encode(input_str) == expected

def test_null_char_data():
    input_str = "\x00\x01\x02"  # binary
    expected = "AAEC"
    assert base64_encode(input_str) == expected

def test_padding_with_two_equals():
    input_str = "M"
    expected = "TQ=="
    assert base64_encode(input_str) == expected

def test_padding_with_one_equal():
    input_str = "Ma"
    expected = "TWE="
    assert base64_encode(input_str) == expected