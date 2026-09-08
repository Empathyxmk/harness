from src.ajpfuzzer.ajpfuzzer import Utils
import pytest

def test_random_string_all_chars_edge_different():
    result = Utils.random_string(3, "z")
    assert result == "zzz"

def test_get_random_int_min_greater_than_max_throws_different():
    with pytest.raises(ValueError):
        Utils.get_random_int(10, 2)

def test_create_map_from_pairs_type_safety_different():
    m = Utils.create_map_from_pairs("x", 0.1, "y", 2.2)
    assert m["x"] == 0.1
    assert m["y"] == 2.2

def test_to_hex_upper_byte_values_different():
    arr = bytes([0xde, 0xad, 0xbe, 0xef])
    hexed = Utils.to_hex(arr)
    assert hexed == "deadbeef"

def test_join_with_only_one_element_different():
    arr = ["onlyone"]
    assert Utils.join(arr, ",") == "onlyone"