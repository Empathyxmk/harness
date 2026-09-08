import pytest
from EvoloPy.optimizer import selector

def test_de_public_valid():
    func_details = ['F5', -20, 20, 10]
    popSize = 7
    Iter = 3
    algo = selector("DE", func_details, popSize, Iter)
    assert hasattr(algo, 'fitness') or hasattr(algo, 'convergence')

def test_de_public_invalid():
    func_details = ['F5', -20, 20, 10]
    result = selector("DE_BOGUS", func_details, 8, 2)
    assert result is None or result is False