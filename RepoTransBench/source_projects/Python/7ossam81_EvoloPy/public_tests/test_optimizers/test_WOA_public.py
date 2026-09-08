import pytest
from EvoloPy.optimizer import selector

def test_woa_public_valid():
    func_details = ['F16', -60, 60, 16]
    popSize = 7
    Iter = 7
    algo = selector("WOA", func_details, popSize, Iter)
    assert hasattr(algo, 'fitness') or hasattr(algo, 'convergence')

def test_woa_public_invalid():
    func_details = ['F16', -60, 60, 16]
    result = selector("WOA_NOPS", func_details, 7, 7)
    assert result is None or result is False