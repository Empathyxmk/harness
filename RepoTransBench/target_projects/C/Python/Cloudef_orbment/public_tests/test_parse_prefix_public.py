import pytest
from src import parse_prefix

def buf_to_str(buf):
    return ''.join(buf)

def test_parse_prefix_basic_public():
    output = []
    ret = parse_prefix.parse_prefix("xyz123", output, 20)
    assert ret == 0
    assert buf_to_str(output) == "xyz123"

def test_parse_prefix_null_input_public():
    output = []
    ret = parse_prefix.parse_prefix(None, output, 8)
    assert ret == -1

def test_parse_prefix_null_output_public():
    ret = parse_prefix.parse_prefix("test", None, 5)
    assert ret == -1

def test_parse_prefix_overflow_public():
    output = []
    ret = parse_prefix.parse_prefix("overflow", output, 4)
    assert ret == -2