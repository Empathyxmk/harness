import pytest

def shell_sort(a, l, r):
    n = r - l + 1
    gap = n // 2
    while gap > 0:
        for i in range(l + gap, l + n):
            temp = a[i]
            j = i
            while j >= l + gap and a[j - gap] > temp:
                a[j] = a[j - gap]
                j -= gap
            a[j] = temp
        gap = gap // 2

def check(a, b, n):
    return all(a[i] == b[i] for i in range(n))

def test_shell_basic():
    a = [14, 2, 6, 4, 11, 7]
    exp = [2, 4, 6, 7, 11, 14]
    shell_sort(a, 0, 5)
    assert a == exp

def test_shell_sorted():
    a = [1, 2, 3, 4, 5]
    exp = [1, 2, 3, 4, 5]
    shell_sort(a, 0, 4)
    assert a == exp

def test_shell_reverse():
    a = [8, 6, 4, 2]
    exp = [2, 4, 6, 8]
    shell_sort(a, 0, 3)
    assert a == exp

def test_shell_equal():
    a = [9, 9, 9]
    exp = [9, 9, 9]
    shell_sort(a, 0, 2)
    assert a == exp