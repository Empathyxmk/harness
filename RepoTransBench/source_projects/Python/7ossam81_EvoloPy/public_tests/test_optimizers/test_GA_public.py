import pytest
from EvoloPy.optimizer import selector

def test_ga_public_valid():
    func_details = ['F7', -33, 33, 17]
    popSize = 6
    Iter = 10
    algo = selector("GA", func_details, popSize, Iter)
    assert hasattr(algo, 'fitness') or hasattr(algo, 'convergence')

def test_ga_public_invalid():
    func_details = ['F7', -33, 33, 17]
    result = selector("GA_FAKE", func_details, 6, 10)
    assert result is None or result is False