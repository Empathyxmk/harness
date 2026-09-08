import pytest
from EvoloPy.optimizer import selector

def test_hho_public_valid():
    func_details = ['F3', -100, 100, 8]
    popSize = 3
    Iter = 7
    algo = selector("HHO", func_details, popSize, Iter)
    assert hasattr(algo, 'fitness') or hasattr(algo, 'convergence')

def test_hho_public_invalid():
    func_details = ['F3', -100, 100, 8]
    result = selector("HHO_UNKNOWN", func_details, 3, 7)
    assert result is None or result is False