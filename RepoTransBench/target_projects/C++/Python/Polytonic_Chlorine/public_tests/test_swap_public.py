import pytest

def cpu_swap(spam, eggs):
    for i in range(len(spam)):
        tmp = spam[i]
        spam[i] = eggs[i]
        eggs[i] = tmp

def test_swap_public():
    spam = [1.23, 4.56, 7.89]
    eggs = [9.87, 6.54, 3.21]
    cpu_swap(spam, eggs)
    assert spam == [9.87, 6.54, 3.21]
    assert eggs == [1.23, 4.56, 7.89]

def test_swap_public_empty():
    spam = []
    eggs = []
    cpu_swap(spam, eggs)
    assert spam == [] and eggs == []