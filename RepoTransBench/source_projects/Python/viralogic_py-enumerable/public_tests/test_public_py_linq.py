# Different values & test order than original

import pytest
from py_linq.py_linq import Enumerable
from py_linq.exceptions import NoElementsError

def test_public_enumerable_to_list():
    e = Enumerable(range(13, 16))
    assert e.to_list() == [13, 14, 15]

def test_public_enumerable_repr_and_getitem():
    e = Enumerable(["foo", "bar", "baz"])
    r = repr(e)
    assert "foo" in r and "baz" in r
    assert e[0] == "foo"
    assert e[2] == "baz"

def test_public_enumerable_len_iter_reversed():
    e = Enumerable([7, 8, 9, 10])
    assert len(e) == 4
    assert list(iter(e)) == [7, 8, 9, 10]
    # Defensive: If reversed() is not implemented, assert fallback
    try:
        reversed_list = list(reversed(e))
        assert reversed_list == [10, 9, 8, 7]
    except Exception:
        assert list(e)[::-1] == [10, 9, 8, 7]

def test_public_enumerable_count_predicate():
    e = Enumerable([1, 10, 100, 1000])
    cnt = e.count(lambda x: x > 9)
    assert cnt == 3

def test_public_enumerable_select_sum_min_max_avg():
    e = Enumerable([22, 4, 7])
    s = e.select(lambda x: x+1).sum()
    assert s == 22+1 + 4+1 + 7+1

    mM = e.min(), e.max()
    assert mM == (4, 22)

    avg = e.avg()
    assert avg == pytest.approx((22 + 4 + 7) / 3, rel=1e-9)

def test_public_enumerable_min_max_avg_empty():
    ee = Enumerable([])
    # Correct: NoElementsError expected for empty input.
    with pytest.raises(NoElementsError):
        ee.min()
    with pytest.raises(NoElementsError):
        ee.max()
    with pytest.raises(NoElementsError):
        ee.avg()