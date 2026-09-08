import pytest
from src.modules.pie.pie import slices

def test_slices_positive_n():
    assert slices(3) == [1, 2, 3]

def test_slices_n_less_than_1():
    assert slices(0) == []
    assert slices(-1) == []

def test_slices_non_number():
    assert slices("foo") == []
    assert slices() == []