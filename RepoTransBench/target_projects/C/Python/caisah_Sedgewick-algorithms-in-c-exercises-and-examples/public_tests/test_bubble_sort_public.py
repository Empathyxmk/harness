import pytest

def bubble_sort(a, n):
    for i in range(n - 1):
        for j in range(n - i - 1):
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]

def test_bubble_sort():
    # All unique random
    arr = [21, 17, -8, 3, 5]
    expected = [-8, 3, 5, 17, 21]
    bubble_sort(arr, 5)
    assert arr == expected

    # array with duplicates
    arr = [10, 10, 5, 7, 5]
    expected = [5, 5, 7, 10, 10]
    bubble_sort(arr, 5)
    assert arr == expected

    # Already sorted
    arr = [1,2,3,4]
    expected = [1,2,3,4]
    bubble_sort(arr, 4)
    assert arr == expected

    # Two elements, reverse
    arr = [9,2]
    bubble_sort(arr,2)
    assert arr == [2,9]

    # One element
    arr = [-1234]
    bubble_sort(arr,1)
    assert arr == [-1234]

    # Zeros and negative
    arr = [0,0,0,0,0,-1]
    expected = [-1,0,0,0,0,0]
    bubble_sort(arr,6)
    assert arr == expected