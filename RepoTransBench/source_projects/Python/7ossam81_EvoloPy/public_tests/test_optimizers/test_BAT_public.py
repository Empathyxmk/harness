import pytest
from EvoloPy.optimizer import selector

def test_bat_public_valid():
    func_details = ['F8', -50, 50, 10]
    popSize = 6
    Iter = 8
    algo = selector("BAT", func_details, popSize, Iter)
    assert hasattr(algo, 'fitness') or hasattr(algo, 'convergence')

def test_bat_public_invalid():
    func_details = ['F8', -50, 50, 10]
    result = selector("BAT_WRONG", func_details, 6, 8)
    assert result is None or result is False