def filter_evens(nums):
    return [n for n in nums if n % 2 == 0]

def test_evens_public_simple():
    assert filter_evens([2, 3, 4, 5]) == [2, 4]

def test_evens_public_none():
    assert filter_evens([1, 3, 5]) == []

def test_evens_public_all():
    assert filter_evens([2, 4, 6]) == [2, 4, 6]