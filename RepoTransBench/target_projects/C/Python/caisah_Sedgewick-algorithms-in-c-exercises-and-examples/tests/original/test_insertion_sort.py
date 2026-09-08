import pytest

def insertion_sort(a, l, r):
    for i in range(l + 1, r + 1):
        key = a[i]
        j = i - 1
        while j >= l and a[j] > key:
            a[j+1] = a[j]
            j -= 1
        a[j+1] = key

def test_random():
    a = [5, 2, 9, 3, 1]
    expected = [1, 2, 3, 5, 9]
    insertion_sort(a, 0, 4)
    assert a == expected

def test_sorted():
    a = [1, 2, 3, 4]
    expected = [1, 2, 3, 4]
    insertion_sort(a, 0, 3)
    assert a == expected

def test_reverse():
    a = [4, 3, 2, 1]
    expected = [1, 2, 3, 4]
    insertion_sort(a, 0, 3)
    assert a == expected

def test_equal():
    a = [2, 2, 2]
    expected = [2, 2, 2]
    insertion_sort(a, 0, 2)
    assert a == expected

def test_single():
    a = [42]
    expected = [42]
    insertion_sort(a, 0, 0)
    assert a == expected