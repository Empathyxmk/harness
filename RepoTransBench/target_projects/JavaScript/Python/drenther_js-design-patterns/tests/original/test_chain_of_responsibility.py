import pytest

def import_chain_sum():
    # Assume presence of ChainOfResponsibility.py in src/Behavioral/ChainOfResponsibility.py
    from src.Behavioral.ChainOfResponsibility import CumulativeSum
    return CumulativeSum

def test_initial_value_add_values_and_chain():
    CumulativeSum = import_chain_sum()
    sum_obj = CumulativeSum(2)
    assert sum_obj.sum == 2
    sum_obj.add(3)
    assert sum_obj.sum == 5
    sum_obj.add(-2).add(7)
    assert sum_obj.sum == 10

def test_default_initial_value_zero():
    CumulativeSum = import_chain_sum()
    sum_obj = CumulativeSum()
    assert sum_obj.sum == 0

def test_method_chaining_works():
    CumulativeSum = import_chain_sum()
    sum_obj = CumulativeSum()
    sum_obj.add(1).add(4).add(5)
    assert sum_obj.sum == 10