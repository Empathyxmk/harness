import pytest
from EvoloPy.optimizer import selector

def test_ssa_public_valid():
    func_details = ['F6', -200, 200, 11]
    popSize = 5
    Iter = 10
    algo = selector("SSA", func_details, popSize, Iter)
    assert hasattr(algo, 'fitness') or hasattr(algo, 'convergence')

def test_ssa_public_invalid():
    func_details = ['F6', -200, 200, 11]
    result = selector("SSA_NOPE", func_details, 5, 10)
    assert result is None or result is False