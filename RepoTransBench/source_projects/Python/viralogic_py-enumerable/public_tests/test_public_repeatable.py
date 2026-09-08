from py_linq.core import RepeatableIterable

def test_public_repeatable_common_usage():
    items = RepeatableIterable([10, 20, 30])
    # Do several repeated actions with different numbers than private test
    assert list(items) == [10, 20, 30]
    assert list(items) == [10, 20, 30]
    assert sum(items) == 60
    assert any(x > 25 for x in items)
    assert all(x < 40 for x in items)