import pytest
from src.testing_sets import set_difference

def test_set_difference_no_overlap_non_null():
    set1 = {1}
    set2 = {2}
    result = set_difference(set(set1), set2)
    assert result is not None
    assert result == set1

def test_set_difference_set2_empty():
    set1 = {3}
    set2 = set()
    result = set_difference(set(set1), set2)
    assert result is not None
    assert result == set1

def test_set_difference_with_overlap():
    set1 = {1, 2, 3}
    set2 = {2, 4}
    expected = {1, 3}
    result = set_difference(set(set1), set2)
    assert result == expected

def test_set_difference_set1_empty_set2_non_empty():
    set1 = set()
    set2 = {4}
    result = set_difference(set(set1), set2)
    assert result is None

def test_set_difference_set1_null():
    set2 = {1}
    with pytest.raises(TypeError):
        set_difference(None, set2)

def test_set_difference_set2_null():
    set1 = {2}
    with pytest.raises(TypeError):
        set_difference(set1, None)

def test_set_difference_both_null():
    with pytest.raises(TypeError):
        set_difference(None, None)

def test_set_difference_all_elements_removed():
    set1 = {10, 20}
    set2 = {10, 20, 30}
    result = set_difference(set(set1), set2)
    assert result is None

def test_set_difference_both_empty():
    set1 = set()
    set2 = set()
    result = set_difference(set(set1), set2)
    assert result is None

def test_set_difference_identical_sets():
    set1 = {100, 200}
    set2 = {100, 200}
    result = set_difference(set(set1), set2)
    assert result is None