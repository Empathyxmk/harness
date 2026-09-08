def import_chain_sum():
    from src.Behavioral.ChainOfResponsibility import CumulativeSum
    return CumulativeSum

def test_starting_at_5_chain_add_7_neg4_12():
    CumulativeSum = import_chain_sum()
    sum_obj = CumulativeSum(5)
    assert sum_obj.sum == 5
    sum_obj.add(7)
    assert sum_obj.sum == 12
    sum_obj.add(-4).add(12)
    assert sum_obj.sum == 20

def test_default_initial_value_zero_add_multiples():
    CumulativeSum = import_chain_sum()
    sum_obj = CumulativeSum()
    assert sum_obj.sum == 0
    sum_obj.add(10).add(-2).add(-8)
    assert sum_obj.sum == 0

def test_method_chaining_with_different_data():
    CumulativeSum = import_chain_sum()
    sum_obj = CumulativeSum()
    sum_obj.add(2).add(3).add(6)
    assert sum_obj.sum == 11