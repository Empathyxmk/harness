import pytest
from src.modules.pie.pie import slices

def test_slices_positive_new():
    assert slices(5) == [1, 2, 3, 4, 5]

def test_slices_n_less_than_1_different():
    assert slices(-2) == []
    assert slices(0) == []

def test_slices_non_number_additional():
    assert slices({}) == []
    assert slices([]) == []