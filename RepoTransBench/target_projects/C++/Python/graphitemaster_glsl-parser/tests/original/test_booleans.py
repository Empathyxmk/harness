import pytest

def test_booleans_assignment_and_literals():
    test_uninitialized = None
    test_true_initialized = True
    test_false_initialized = False
    test_assign = None
    test_assign = test_true_initialized
    assert test_assign is True
    test_assign = test_false_initialized
    assert test_assign is False
    test_assign = True
    assert test_assign is True
    test_assign = False
    assert test_assign is False