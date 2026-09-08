import pytest

def count_even(xs):
    return sum(1 for x in xs if x % 2 == 0)

def test_PublicEpollTest_CountEven():
    assert count_even([2,4,6,8,10]) == 5
    assert count_even([1,3,5]) == 0
    assert count_even([9,8,7,6]) == 2

def test_PublicEpollTest_CountEvenEmpty():
    assert count_even([]) == 0
    assert count_even([1]) == 0