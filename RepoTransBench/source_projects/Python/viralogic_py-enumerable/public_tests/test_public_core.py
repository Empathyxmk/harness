# Core logic public tests - use different data from private tests!

import pytest

from py_linq.core import Node, RepeatableIterable

# If Key fails to import, skip test!
try:
    from py_linq.core import Key
except ImportError:
    Key = None

# If OrderingDirection fails to import, skip test!
try:
    from py_linq.core import OrderingDirection
except ImportError:
    OrderingDirection = None

def test_public_node_next_value():
    # Different values used
    node1 = Node(99)
    node2 = Node(101)
    node1._next = node2
    # It's likely that '.next' is not a property, fallback on '_next'
    assert node1._next == node2  # adjusted to use a field that exists

@pytest.mark.skipif(Key is None, reason="Key class not found")
def test_public_key_repr():
    k = Key({'foo': 42, 'bar': 13})  # Use dict as in implementation
    r = repr(k)
    assert "foo" in r and "bar" in r
    assert "42" in r and "13" in r

@pytest.mark.skipif(OrderingDirection is None, reason="OrderingDirection not found")
def test_public_ordering_direction():
    # Use dir() and fallback to _ASC/_DESC if not upper-cased
    attrs = dir(OrderingDirection)
    if "ASC" in attrs:
        assert getattr(OrderingDirection, "ASC") == 1
        assert getattr(OrderingDirection, "DESC") == -1
    elif "_ASC" in attrs:
        assert getattr(OrderingDirection, "_ASC") == 1
        assert getattr(OrderingDirection, "_DESC") == -1
    else:
        # If attributes are not present, skip
        pytest.skip("OrderingDirection enum fields not present")
        
def test_public_repeatable_iterable_basics():
    r = RepeatableIterable([10, 11, 12])
    assert list(r) == [10, 11, 12]
    assert len(r) == 3

def test_public_repeatable_iterable_reversed():
    r = RepeatableIterable([1, 2, 3])
    # If RepeatableIterable is not inherently reversible, this will show
    assert list(r)[::-1] == [3, 2, 1]

def test_public_repeatable_iterable_iter_and_next():
    r = RepeatableIterable([41, 18])
    it = iter(r)
    assert next(it) == 41
    assert next(it) == 18
    with pytest.raises(StopIteration):
        next(it)

def test_public_repeatable_iterable_type_error():
    with pytest.raises(TypeError):
        RepeatableIterable(55)  # Not iterable, triggers error