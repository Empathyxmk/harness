import pytest
from EvoloPy.optimizer import selector

def test_pso_public_valid():
    func_details = ['F10', -25, 25, 14]
    popSize = 8
    Iter = 8
    algo = selector("PSO", func_details, popSize, Iter)
    assert hasattr(algo, 'fitness') or hasattr(algo, 'convergence')

def test_pso_public_invalid():
    func_details = ['F10', -25, 25, 14]
    result = selector("PSO_MISS", func_details, 9, 8)
    assert result is None or result is False