import pytest

def shell_sort(a, n):
    gap = n // 2
    while gap > 0:
        for i in range(gap, n):
            temp = a[i]
            j = i
            while j >= gap and a[j - gap] > temp:
                a[j] = a[j - gap]
                j -= gap
            a[j] = temp
        gap //= 2

def test_shell_sort():
    # Varied positive/negative
    arr = [37, -12, 49, 0, 27, 100, -57, 4]
    expected = [-57, -12, 0, 4, 27, 37, 49, 100]
    shell_sort(arr, 8)
    assert arr == expected

    # Two elements swapped
    arr = [2, 1]
    expected = [1, 2]
    shell_sort(arr, 2)
    assert arr == expected

    # Single
    arr = [-88]
    shell_sort(arr, 1)
    assert arr[0] == -88

    # Large mostly reversed
    arr = [81,70,43,32,25,17,13,3]
    expected = [3,13,17,25,32,43,70,81]
    shell_sort(arr, 8)
    assert arr == expected

    # With zeros & duplicates
    arr = [0,2,2,0,1,0]
    expected = [0,0,0,1,2,2]
    shell_sort(arr, 6)
    assert arr == expected

    # Already sorted
    arr = [3,7,14,89]
    expected = [3,7,14,89]
    shell_sort(arr, 4)
    assert arr == expected