import pytest

def test_public_collections_extra_dummy():
    lst = [10, 2, 7, 4, 2]
    s = set(lst)
    assert len(s) == 4
    assert sorted(s) == [2, 4, 7, 10]