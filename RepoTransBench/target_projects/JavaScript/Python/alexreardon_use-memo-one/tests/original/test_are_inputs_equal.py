import pytest
from src.are_inputs_equal import are_inputs_equal

def test_returns_true_when_both_arrays_are_empty():
    assert are_inputs_equal([], []) is True

def test_returns_false_when_arrays_have_different_lengths():
    assert are_inputs_equal([1], []) is False
    assert are_inputs_equal([], [1]) is False
    assert are_inputs_equal([1,2], [1]) is False

def test_returns_true_for_shallow_equal_arrays():
    assert are_inputs_equal([1,2,3], [1,2,3]) is True
    assert are_inputs_equal(['a', 'b'], ['a', 'b']) is True
    obj = {}
    # "is" identity is required by ported logic
    assert are_inputs_equal([obj], [obj]) is True

def test_returns_false_if_any_value_differs():
    assert are_inputs_equal([1,2,3], [1,2,4]) is False
    # different references
    assert are_inputs_equal([{'x':1}], [{'x':1}]) is False
    assert are_inputs_equal([None], [None]) is True
    assert are_inputs_equal([None], [0]) is False
    import math
    assert are_inputs_equal([float('nan')], [float('nan')]) is False

def test_returns_true_for_same_reference_arrays():
    arr = [1,2]
    assert are_inputs_equal(arr, arr) is True

def test_returns_false_for_shallow_equal_but_different_reference_objects():
    assert are_inputs_equal([{'x':1}], [{'x':1}]) is False

def test_handles_complex_edge_cases():
    class Foo:
        def __init__(self, v): self.v = v
    a = Foo(1)
    b = Foo(1)
    assert are_inputs_equal([a],[a]) is True
    assert are_inputs_equal([a],[b]) is False
    assert are_inputs_equal([1, "a", None], [1, "a", None]) is True
    assert are_inputs_equal([1,2],[1,2,3]) is False