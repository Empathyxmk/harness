import pytest
from src.assistant.base64_encode import base64_encode

def test_simple_string_public():
    input_str = "TestString"
    expected = "VGVzdFN0cmluZw=="
    assert base64_encode(input_str) == expected

def test_empty_string_public():
    input_str = ""
    expected = ""
    assert base64_encode(input_str) == expected

def test_binary_data_public():
    input_str = "\xE3\x81\x82"  # UTF-8 for 'あ'
    expected = "44GC"
    assert base64_encode(input_str) == expected

def test_padding_case_public():
    input_str = "AB"
    expected = "QUI="
    assert base64_encode(input_str) == expected

def test_multiple_padding_case_public():
    input_str = "A"
    expected = "QQ=="
    assert base64_encode(input_str) == expected