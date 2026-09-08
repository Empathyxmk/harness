import pytest
import re
from src.blueimp_md5 import md5

def test_hash_single_space():
    assert md5(' ') == '7215ee9c7d9dc229d2921a40e899ec5f'

def test_hash_different_ascii():
    assert md5('def') == '4ed9407630eb1000c0f6b63842defa7d'

def test_hash_pangram_without_spaces():
    assert md5('thequickbrownfoxjumpsoverthelazydog') == '5c6ffbdd40d9556b73a21e63c3e0e904'

def test_hash_with_different_key_hmac():
    assert md5('hello', 'world') == 'fa4eeaeb4ec9f72b26e17e30ee466c03'

def test_hash_other_number_as_string():
    assert md5(456) == md5("456")

def test_hash_boolean_true_as_string_repeat():
    assert md5(True) == md5("true")

def test_hash_boolean_false_as_string_repeat():
    assert md5(False) == md5("false")

def test_hash_nan_as_string():
    nan_value = float('nan')
    assert md5(nan_value) == md5("NaN")

def test_hash_null_as_string_repeat():
    assert md5(None) == md5("null")

def test_hash_array_as_string():
    try:
        md5([1,2,3])
    except Exception:
        pytest.fail("md5([1,2,3]) raised exception")

def test_produce_raw_output_third_param_true_other_input():
    hash_val = md5('publicTest', None, True)
    assert isinstance(hash_val, bytes)
    assert len(hash_val) == 16

def test_handle_multibyte_cjk():
    out = md5('漢字')
    assert isinstance(out, str)
    assert len(out) == 32

def test_empty_key_hmac_equivalent_no_key_different_input():
    assert md5('def', '') == md5('def')

def test_produce_different_results_with_key_public_input():
    assert md5('def', 'differentKey') != md5('def')

def test_not_throw_date_input():
    import datetime
    try:
        md5(datetime.datetime.now())
    except Exception:
        pytest.fail("md5(datetime) raised exception")

def test_hash_buffer_different_content_node_buffer_shim():
    buf = b'test'
    assert md5(buf) == '098f6bcd4621d373cade4e832627b4f6'

def test_output_hex_when_raw_is_false_different_input():
    out = md5('blue', None, False)
    assert re.match(r"^[\da-f]{32}$", out)

def test_output_raw_when_raw_eq_1_public_input():
    raw = md5('another', None, 1)
    assert isinstance(raw, bytes)
    assert len(raw) == 16

def test_treat_undefined_raw_param_as_hex_public_input():
    out = md5('different', None, None)
    assert re.match(r"^[\da-f]{32}$", out)

def test_treat_key_as_number():
    out = md5('def', 42)
    assert isinstance(out, str)
    assert len(out) == 32

def test_hash_with_key_and_16_byte_output_in_raw_public():
    raw = md5('world', 'hello', True)
    assert isinstance(raw, bytes)
    assert len(raw) == 16