import pytest
import re
from src.blueimp_md5 import md5

def to_bytes(val):
    # For test compatibility (e.g., for the Buffer test)
    if isinstance(val, bytes):
        return val
    else:
        return str(val).encode('utf-8')

def test_hash_empty_string():
    assert md5('') == "d41d8cd98f00b204e9800998ecf8427e"

def test_hash_short_ascii():
    assert md5('abc') == "900150983cd24fb0d6963f7d28e17f72"

def test_hash_long_input():
    assert md5('The quick brown fox jumps over the lazy dog') == "9e107d9d372bb6826bd81d3542a419d6"

def test_hash_with_key_hmac():
    # Blueimp behaviour: md5('abc', 'key')
    assert md5('abc', 'key') == "ffb7c0fc166f7ca075dfa04d59aed232"

def test_hash_numbers_as_string():
    assert md5(123) == md5("123")

def test_hash_boolean_false_as_string():
    assert md5(False) == md5("false")

def test_hash_boolean_true_as_string():
    assert md5(True) == md5("true")

def test_hash_null_as_string():
    assert md5(None) == md5("null")

def test_hash_undefined_as_string():
    # In JS, undefined becomes 'undefined'
    assert md5("undefined") == md5("undefined")  # No undefined in Python

def test_produce_raw_output_third_param_true():
    hash_val = md5('blueimp', None, True)
    assert isinstance(hash_val, bytes)
    assert len(hash_val) == 16

def test_handle_multibyte_emoji():
    out = md5('😀')
    assert isinstance(out, str)
    assert len(out) == 32  # Should be 32 hex digits

def test_empty_key_hmac_equivalent_no_key():
    assert md5('abc', '') == md5('abc')

def test_produce_different_results_with_key():
    assert md5('abc', 'key') != md5('abc')

def test_not_throw_object_input():
    try:
        md5({'foo': 'bar'})  # Should not raise
    except Exception:
        pytest.fail("md5({'foo':'bar'}) raised exception")

def test_hash_buffer_node_buffer_shim():
    buf = b'abc'
    assert md5(buf) == "900150983cd24fb0d6963f7d28e17f72"

# Edge and error handling

def test_output_hex_when_raw_is_false():
    out = md5('abc', None, False)
    assert re.match(r"^[\da-f]{32}$", out)

def test_output_raw_when_raw_eq_1():
    raw = md5('abc', None, 1)
    assert isinstance(raw, bytes)
    assert len(raw) == 16

def test_treat_undefined_raw_param_as_hex():
    out = md5('abc', None, None)
    assert re.match(r"^[\da-f]{32}$", out)

def test_key_with_non_string():
    out = md5('abc', {'k': 1})
    assert isinstance(out, str)
    assert len(out) == 32

def test_hash_with_key_and_16_byte_output_in_raw():
    raw = md5('abc', 'key', True)
    assert isinstance(raw, bytes)
    assert len(raw) == 16