import pytest
from src.are_inputs_equal import are_inputs_equal

def test_returns_true_for_two_empty_arrays():
    assert are_inputs_equal([], []) is True

def test_returns_false_for_arrays_of_different_lengths():
    assert are_inputs_equal([1,2], [1,2,3]) is False

def test_returns_false_if_one_element_is_different():
    assert are_inputs_equal([5, 'c', None], [5, 'c', 0]) is False

def test_returns_true_if_arrays_contain_same_references_for_objects():
    ref = {'b': 2}
    assert are_inputs_equal([ref, 8], [ref, 8]) is True

def test_returns_false_for_deep_but_non_reference_equality_on_objects():
    assert are_inputs_equal([{'p':2}], [{'p':2}]) is False