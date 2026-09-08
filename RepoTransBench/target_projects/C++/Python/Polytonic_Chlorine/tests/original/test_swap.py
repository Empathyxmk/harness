import pytest

def cpu_swap(spam, eggs):
    for i in range(len(spam)):
        tmp = spam[i]
        spam[i] = eggs[i]
        eggs[i] = tmp

def test_swap_basic():
    spam = [3.14] * 3
    eggs = [2.72] * 3
    cpu_swap(spam, eggs)
    for f in spam:
        assert f == 2.72
    for f in eggs:
        assert f == 3.14

def test_swap_empty():
    spam = []
    eggs = []
    cpu_swap(spam, eggs)
    assert spam == [] and eggs == []