import pytest
from EvoloPy.optimizer import selector

def test_ffa_public_valid():
    func_details = ['F9', -100, 100, 7]
    popSize = 9
    Iter = 9
    algo = selector("FFA", func_details, popSize, Iter)
    assert hasattr(algo, 'fitness') or hasattr(algo, 'convergence')

def test_ffa_public_invalid():
    func_details = ['F9', -100, 100, 7]
    result = selector("FFA_NOTREAL", func_details, 9, 9)
    assert result is None or result is False