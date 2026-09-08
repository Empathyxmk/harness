import pytest

def insertion_sort(a, n):
    for i in range(1, n):
        key = a[i]
        j = i - 1
        while j >= 0 and a[j] > key:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = key

def test_insertion_sort():
    # All negative and positive
    arr = [12, -9, 0, 42, -3, 25]
    expected = [-9, -3, 0, 12, 25, 42]
    insertion_sort(arr, 6)
    assert arr == expected

    # Reverse sorted array
    arr = [7, 6, 5, 4, 3, 2, 1]
    expected = [1, 2, 3, 4, 5, 6, 7]
    insertion_sort(arr, 7)
    assert arr == expected

    # With duplicates and large
    arr = [99, -8, -8, 0, 1, 44, 44, 3]
    expected = [-8, -8, 0, 1, 3, 44, 44, 99]
    insertion_sort(arr, 8)
    assert arr == expected

    # Already sorted
    arr = [2, 4, 8, 16, 32]
    expected = [2, 4, 8, 16, 32]
    insertion_sort(arr, 5)
    assert arr == expected

    # Single, zero/empty
    arr = [11]
    insertion_sort(arr, 1)
    assert arr[0] == 11

    # all same
    arr = [5,5,5,5]
    insertion_sort(arr, 4)
    assert arr == [5,5,5,5]

    # descending with negatives
    arr = [10,0,-5,-12]
    expected = [-12,-5,0,10]
    insertion_sort(arr, 4)
    assert arr == expected