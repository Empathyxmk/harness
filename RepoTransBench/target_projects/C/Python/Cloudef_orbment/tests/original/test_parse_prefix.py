import pytest
from src import parse_prefix

def buf_to_str(buf):
    return ''.join(buf)

def test_parse_prefix_basic():
    output = []
    ret = parse_prefix.parse_prefix("abc", output, 16)
    assert ret == 0
    assert buf_to_str(output) == "abc"

def test_parse_prefix_null_input():
    output = []
    ret = parse_prefix.parse_prefix(None, output, 16)
    assert ret == -1

def test_parse_prefix_null_output():
    ret = parse_prefix.parse_prefix("abc", None, 4)
    assert ret == -1

def test_parse_prefix_overflow():
    output = []
    ret = parse_prefix.parse_prefix("abc", output, 2)  # need 4 (abc\0)
    assert ret == -2