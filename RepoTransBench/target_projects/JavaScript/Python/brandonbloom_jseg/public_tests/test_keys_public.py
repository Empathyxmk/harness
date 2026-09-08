import pytest

def unique_keys(lst):
    """
    Returns True if all keys in the list are unique.
    Assumes lst is a list of strings or hashable types.
    """
    return len(set(lst)) == len(lst)

def test_unique_keys_true():
    keys = ["a", "b", "c", "d"]
    assert unique_keys(keys)
    keys = [1, 2, 3, 4]
    assert unique_keys(keys)
    keys = []
    assert unique_keys(keys)

def test_unique_keys_false():
    keys = ["a", "b", "a"]
    assert not unique_keys(keys)
    keys = [1, 2, 2, 3]
    assert not unique_keys(keys)
    keys = ["", ""]
    assert not unique_keys(keys)

def test_edge_cases():
    keys = ["a", "A"]  # different due to case
    assert unique_keys(keys)
    keys = [None, "None", None]
    assert not unique_keys(keys)