import pytest
from py_linq.py_linq import Enumerable
from py_linq.exceptions import NoElementsError

def test_enumerable_to_list():
    e = Enumerable([1,2,3])
    assert e.to_list() == [1,2,3]

def test_enumerable_repr_and_getitem():
    e = Enumerable([10,11,12])
    r = repr(e)
    assert isinstance(r, str)
    assert e[1] == 11

def test_enumerable_len_iter_reversed():
    e = Enumerable([1,2,3,4])
    assert len(e) == 4
    assert list(iter(e)) == [1,2,3,4]
    assert list(reversed(e)) == [4,3,2,1]

def test_enumerable_count_predicate():
    e = Enumerable([1,2,3,4])
    assert e.count(lambda x: x > 2) == 2
    assert e.count() == 4

def test_enumerable_select_sum_min_max_avg():
    e = Enumerable([1,2,3])
    selected = e.select(lambda x: x*2)
    assert selected.to_list() == [2,4,6]
    assert e.sum() == 6
    assert e.sum(lambda x: x+1) == 9
    assert e.min() == 1
    assert e.max() == 3
    assert e.avg() == pytest.approx(2.0)
    assert e.avg(lambda x: x + 1) == pytest.approx(3.0)

def test_enumerable_min_max_avg_empty():
    e = Enumerable([])
    with pytest.raises(NoElementsError):
        e.min()
    with pytest.raises(NoElementsError):
        e.max()
    with pytest.raises(NoElementsError):
        e.avg()