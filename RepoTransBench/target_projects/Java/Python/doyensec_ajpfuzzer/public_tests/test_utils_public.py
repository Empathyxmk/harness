import pytest
import re
from src.ajpfuzzer.ajpfuzzer import Utils

def test_random_string_negative_length_different():
    with pytest.raises(ValueError):
        Utils.random_string(-5, "xyz")

def test_random_string_with_empty_chars_different():
    with pytest.raises(ValueError):
        Utils.random_string(3, "")

def test_random_string_with_valid_different_input():
    result = Utils.random_string(6, "wxyz")
    assert result is not None
    assert len(result) == 6
    assert re.match(r"^[wxyz]{6}$", result)

def test_get_random_int_edge_cases_different():
    assert Utils.get_random_int(7,7) == 7
    assert Utils.get_random_int(100,100) == 100

def test_get_random_int_range_different():
    for _ in range(50):
        result = Utils.get_random_int(20,30)
        assert 20 <= result <= 30

def test_create_map_from_pairs_even_arguments_different():
    map_ = Utils.create_map_from_pairs("key1", 555, "key2", 789, "key3", "value3")
    assert len(map_) == 3
    assert map_["key1"] == 555
    assert map_["key2"] == 789
    assert map_["key3"] == "value3"

def test_create_map_from_pairs_odd_arguments_different():
    with pytest.raises(ValueError):
        Utils.create_map_from_pairs("foo", "bar", "baz")

def test_to_hex_different():
    b = bytes([1,11,17,22,51,128,200])
    hexed = Utils.to_hex(b)
    assert re.match(r"^[0-9a-f]{14}$", hexed)
    assert hexed == "010b11163380c8"

def test_to_hex_null_different():
    assert Utils.to_hex(None) is None

def test_to_hex_empty_different():
    assert Utils.to_hex(b"") == ""

def test_join_simple_different():
    arr = ["foo", "bar", "baz"]
    result = Utils.join(arr, "-")
    assert result == "foo-bar-baz"

def test_join_null_different():
    assert Utils.join(None, "&") == ""

def test_join_empty_array_different():
    assert Utils.join([], "~") == ""

def test_join_no_separator_different():
    arr = ["d", "e", "f"]
    assert Utils.join(arr, "") == "def"