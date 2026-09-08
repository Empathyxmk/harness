import pytest

from src.ajpfuzzer.ajpfuzzer import Utils

def test_random_string_all_chars_edge():
    result = Utils.random_string(5, "x")
    assert result == "xxxxx"

def test_get_random_int_min_greater_than_max_throws():
    with pytest.raises(ValueError):
        Utils.get_random_int(5, 2)

def test_create_map_from_pairs_type_safety():
    m = Utils.create_map_from_pairs(1, "a", 2, "b")
    assert m[1] == "a"
    assert m[2] == "b"

def test_to_hex_upper_byte_values():
    arr = bytes([0xaf, 0xff, 0xb4])
    hexed = Utils.to_hex(arr)
    assert hexed == "afffb4"

def test_join_with_only_one_element():
    arr = ["solo"]
    assert Utils.join(arr, ",") == "solo"