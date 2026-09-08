import pytest
from EvoloPy.optimizer import selector

def test_gwo_public_valid():
    func_details = ['F13', -30, 30, 5]
    popSize = 7
    Iter = 6
    algo = selector("GWO", func_details, popSize, Iter)
    assert hasattr(algo, 'fitness') or hasattr(algo, 'convergence')

def test_gwo_public_invalid():
    func_details = ['F13', -30, 30, 5]
    result = selector("GWO_UNKNOWN", func_details, 7, 6)
    assert result is None or result is False