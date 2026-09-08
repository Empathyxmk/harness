import pytest
from py_linq.core import Node, Key, OrderingDirection, RepeatableIterable

def test_node_next_value():
    n1 = Node(1)
    n2 = Node(2)
    n1.next = n2
    assert n1.value == 1
    assert n1.next.value == 2

def test_key_repr():
    k = Key({'a': 1, 'b': 2})
    r = repr(k)
    assert "'a': 1" in r and "'b': 2" in r

    k2 = Key(None, c=3, d=4)
    assert k2.c == 3 and k2.d == 4

def test_ordering_direction():
    od = OrderingDirection(lambda x: -x, True)
    assert od.descending is True
    assert od.key(3) == -3

def test_repeatable_iterable_basics():
    data = [1, 2, 3]
    rit = RepeatableIterable(data)
    out = list(iter(rit))
    assert out == data
    assert len(rit) == 3

def test_repeatable_iterable_reversed():
    data = [1, 2, 3]
    rit = RepeatableIterable(data)
    out = list(reversed(rit))
    assert out == [3, 2, 1]

def test_repeatable_iterable_iter_and_next():
    data = [10, 20, 30]
    rit = RepeatableIterable(data)
    it = iter(rit)
    result = next(it)
    assert result == 10
    # Exhaust all
    for _ in it:
        pass
    # Reset and check again
    assert list(rit) == data

def test_repeatable_iterable_type_error():
    with pytest.raises(TypeError):
        RepeatableIterable(123)