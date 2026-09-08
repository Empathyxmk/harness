import pytest
from EvoloPy.optimizer import selector

def test_mfo_public_valid():
    func_details = ['F15', -40, 40, 13]
    popSize = 10
    Iter = 5
    algo = selector("MFO", func_details, popSize, Iter)
    assert hasattr(algo, 'fitness') or hasattr(algo, 'convergence')

def test_mfo_public_invalid():
    func_details = ['F15', -40, 40, 13]
    result = selector("MFO_FAKE", func_details, 10, 5)
    assert result is None or result is False