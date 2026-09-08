import pytest
from src.assert_util import ok, equal, deepEqual, notDeepEqual

def test_assert_ok():
    ok(456)
    with pytest.raises(AssertionError):
        ok(False)

def test_assert_equal():
    equal("abc", "abc")
    with pytest.raises(AssertionError):
        equal("abc", "def")

def test_assert_deepEqual():
    deepEqual([9], [9])
    with pytest.raises(AssertionError):
        deepEqual([9], [10])

def test_assert_notDeepEqual():
    notDeepEqual([1, 2], [2, 1])
    with pytest.raises(AssertionError):
        notDeepEqual([3], [3])