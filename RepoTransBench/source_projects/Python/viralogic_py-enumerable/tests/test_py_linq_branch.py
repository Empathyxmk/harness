import pytest
from py_linq.py_linq import Enumerable
from py_linq.py_linq import NoElementsError, NullArgumentError

def test_getitem_out_of_range():
    e = Enumerable([1, 2, 3])
    assert e[10] is None  # Hit the branch where n > number of elements

def test_count_predicate_none_vs_func():
    data = [4,5,6]
    e = Enumerable(data)
    cnt_pred = e.count(lambda x: x > 4)
    cnt = e.count()
    assert cnt_pred == 2
    assert cnt == len(data)

def test_repr_non_ascii():
    obj = [{"á": 1}, {"β": 2}]
    e = Enumerable(obj)
    r = repr(e)
    assert isinstance(r, str)
    assert "á" in r and "β" in r

def test_select_identity_vs_func():
    e1 = Enumerable([4, 5])
    assert e1.select().to_list() == [4, 5]
    e2 = Enumerable([4, 5])
    l = e2.select(lambda x: x + 3).to_list()
    assert l == [7, 8]

def test_sum_with_func():
    data = [1, 2, 3]
    e = Enumerable(data)
    total = e.sum(lambda x: x*3)
    assert total == 18

def test_min_max_with_func():
    data = [3, 2, 5]
    e = Enumerable(data)
    result_min = e.min(lambda x: -x)
    result_max = e.max(lambda x: -x)
    # -5 = min (so max=5), -2=max (so min=2)
    assert result_min == -5
    assert result_max == -2

def test_next_dunder_next():
    e = Enumerable([10,20])
    it = iter(e)
    assert next(it) == 10
    assert next(it) == 20
    with pytest.raises(StopIteration):
        next(it)

def test_enumerable_empty_avg():
    e = Enumerable([])
    with pytest.raises(NoElementsError):
        e.avg(lambda x: x*x)