import pytest

def bubble(a, l, r):
    for i in range(l, r):
        for j in range(l, r - (i - l)):
            if a[j] > a[j+1]:
                a[j], a[j+1] = a[j+1], a[j]

def bubble_improved(a, l, r):
    for i in range(l, r):
        swapped = False
        for j in range(l, r - (i - l)):
            if a[j] > a[j+1]:
                a[j], a[j+1] = a[j+1], a[j]
                swapped = True
        if not swapped:
            break

def check(a, b, n):
    return all(a[i] == b[i] for i in range(n))

def test_bubble_basic():
    a = [5, 4, 3, 2, 1, 0]
    exp = [0, 1, 2, 3, 4, 5]
    bubble(a, 0, 5)
    assert a == exp

def test_bubble_already_sorted():
    a = [1, 2, 3, 4, 5]
    exp = [1, 2, 3, 4, 5]
    bubble(a, 0, 4)
    assert a == exp

def test_bubble_improved_basic():
    a = [5, 4, 3, 2, 1, 0]
    exp = [0, 1, 2, 3, 4, 5]
    bubble_improved(a, 0, 5)
    assert a == exp

def test_bubble_improved_already_sorted():
    a = [1, 2, 3, 4, 5]
    exp = [1, 2, 3, 4, 5]
    bubble_improved(a, 0, 4)
    assert a == exp

def test_bubble_duplicates():
    a = [2, 3, 3, 1, 2, 0]
    exp = [0, 1, 2, 2, 3, 3]
    bubble(a, 0, 5)
    assert a == exp