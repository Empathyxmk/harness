import pytest
from src.findindex import findindex

def test_value_found():
    arr = [10, 20, 30, 40, 50]
    val = 30
    expected_idx = 3
    assert findindex(val, arr) == expected_idx

    val = 10
    expected_idx = 1
    assert findindex(val, arr) == expected_idx

    val = 50
    expected_idx = 5
    assert findindex(val, arr) == expected_idx

def test_value_not_found():
    arr = [10, 20, 30, 40, 50]
    val = 99
    expected_idx = 0
    assert findindex(val, arr) == expected_idx

def test_empty_array():
    arr = []
    val = 1
    expected_idx = 0
    assert findindex(val, arr) == expected_idx

def test_single_element_array_found():
    arr = [5]
    val = 5
    expected_idx = 1
    assert findindex(val, arr) == expected_idx

def test_single_element_array_not_found():
    arr = [5]
    val = 10
    expected_idx = 0
    assert findindex(val, arr) == expected_idx