import pytest
from src.testing_sets import set_difference

def test_set_difference_no_overlap_non_null_public():
    set1 = {5}
    set2 = {7}
    result = set_difference(set(set1), set2)
    assert result is not None
    assert result == set1

def test_set_difference_set2_empty_public():
    set1 = {9}
    set2 = set()
    result = set_difference(set(set1), set2)
    assert result is not None
    assert result == set1

def test_set_difference_with_overlap_public():
    set1 = {11, 13, 15}
    set2 = {13, 17}
    expected = {11, 15}
    result = set_difference(set(set1), set2)
    assert result == expected

def test_set_difference_set1_empty_set2_non_empty_public():
    set1 = set()
    set2 = {21}
    result = set_difference(set(set1), set2)
    assert result is None

def test_set_difference_set1_null_public():
    set2 = {22}
    with pytest.raises(TypeError):
        set_difference(None, set2)

def test_set_difference_set2_null_public():
    set1 = {42}
    with pytest.raises(TypeError):
        set_difference(set1, None)

def test_set_difference_both_null_public():
    with pytest.raises(TypeError):
        set_difference(None, None)

def test_set_difference_all_elements_removed_public():
    set1 = {101, 202}
    set2 = {101, 202, 303}
    result = set_difference(set(set1), set2)
    assert result is None

def test_set_difference_both_empty_public():
    set1 = set()
    set2 = set()
    result = set_difference(set(set1), set2)
    assert result is None

def test_set_difference_identical_sets_public():
    set1 = {333, 444}
    set2 = {444, 333}
    result = set_difference(set(set1), set2)
    assert result is None