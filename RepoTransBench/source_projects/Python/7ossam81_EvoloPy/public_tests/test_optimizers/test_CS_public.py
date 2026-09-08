import pytest
from EvoloPy.optimizer import selector

def test_cs_public_valid():
    func_details = ['F17', -15, 15, 18]
    popSize = 4
    Iter = 11
    algo = selector("CS", func_details, popSize, Iter)
    assert hasattr(algo, 'fitness') or hasattr(algo, 'convergence')

def test_cs_public_invalid():
    func_details = ['F17', -15, 15, 18]
    result = selector("CS_FUZZY", func_details, 4, 11)
    assert result is None or result is False