# Property-based/simple randomness checks
import random

def is_sorted(lst):
    return all(lst[i] <= lst[i+1] for i in range(len(lst)-1))

def test_is_sorted_true():
    assert is_sorted([1, 1, 2, 3])

def test_is_sorted_false():
    assert is_sorted([3, 2, 1]) == False

def test_sort_random_lists():
    for _ in range(10):
        arr = [random.randint(0,100) for _ in range(8)]
        sorted_arr = sorted(arr)
        assert is_sorted(sorted_arr)