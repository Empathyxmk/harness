import pytest

def filter_evens(nums):
    return [n for n in nums if n % 2 == 0]

def square_all(nums):
    return [n * n for n in nums]

def sum_all(nums):
    return sum(nums)

def test_filter_evens_all_even():
    assert filter_evens([2, 4, 6]) == [2, 4, 6]
def test_filter_evens_mixed():
    assert filter_evens([1, 2, 3, 4, 5, 6]) == [2, 4, 6]
def test_filter_evens_none():
    assert filter_evens([1, 3, 5]) == []

def test_square_all():
    assert square_all([1, 2, 3]) == [1, 4, 9]

def test_square_all_empty():
    assert square_all([]) == []

def test_sum_all_simple():
    assert sum_all([1,2,3,4]) == 10

def test_sum_all_empty():
    assert sum_all([]) == 0