import pytest
import re
from src.ajpfuzzer.ajpfuzzer import Utils

def test_random_string_negative_length():
    with pytest.raises(ValueError):
        Utils.random_string(-1, "abc")

def test_random_string_with_empty_chars():
    with pytest.raises(ValueError):
        Utils.random_string(5, "")

def test_random_string_with_valid_input():
    result = Utils.random_string(8, "abcd")
    assert result is not None
    assert len(result) == 8
    assert re.match(r"^[abcd]{8}$", result)

def test_get_random_int_edge_cases():
    assert Utils.get_random_int(5, 5) == 5
    assert Utils.get_random_int(42, 42) == 42

def test_get_random_int_range():
    for _ in range(100):
        result = Utils.get_random_int(10, 20)
        assert 10 <= result <= 20

def test_create_map_from_pairs_even_arguments():
    m = Utils.create_map_from_pairs("k1", 123, "k2", "vv", "k3", None)
    assert len(m) == 3
    assert m["k1"] == 123
    assert m["k2"] == "vv"
    assert m["k3"] is None

def test_create_map_from_pairs_odd_arguments():
    with pytest.raises(ValueError):
        Utils.create_map_from_pairs("a", "b", "c")

def test_to_hex():
    b = bytes([0, 10, 15, 16, 31, 127, 255])
    hexed = Utils.to_hex(b)
    assert re.match(r"^[0-9a-f]{14}$", hexed)
    assert hexed == "000a0f101f7fff"

def test_to_hex_null():
    assert Utils.to_hex(None) is None

def test_to_hex_empty():
    assert Utils.to_hex(b"") == ""

def test_join_simple():
    arr = ["a", "b", "c"]
    result = Utils.join(arr, ":")
    assert result == "a:b:c"

def test_join_null():
    assert Utils.join(None, ",") == ""

def test_join_empty_array():
    assert Utils.join([], "|") == ""

def test_join_no_separator():
    arr = ["x", "y"]
    assert Utils.join(arr, "") == "xy"