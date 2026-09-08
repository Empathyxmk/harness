import pytest
from pythonflow.util import merge_dicts, find_duplicates

def test_merge_dicts_public():
    a = {'e': 1, 'f': 2}
    b = {'g': 3}
    m = merge_dicts(a, b)
    assert m['e'] == 1 and m['f'] == 2 and m['g'] == 3

def test_merge_dicts_conflict_public():
    a = {'z': 1}
    b = {'z': 4}
    with pytest.raises(ValueError):
        merge_dicts(a, b)

def test_find_duplicates_public():
    items = [1, 2, 3, 2, 1, 5, 5]
    dups = find_duplicates(items)
    assert set(dups) == {1, 2, 5}