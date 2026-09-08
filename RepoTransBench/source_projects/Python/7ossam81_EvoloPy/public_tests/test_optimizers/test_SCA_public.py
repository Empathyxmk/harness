import pytest
from EvoloPy.optimizer import selector

def test_sca_public_valid():
    func_details = ['F18', -75, 75, 20]
    popSize = 12
    Iter = 8
    algo = selector("SCA", func_details, popSize, Iter)
    assert hasattr(algo, 'fitness') or hasattr(algo, 'convergence')

def test_sca_public_invalid():
    func_details = ['F18', -75, 75, 20]
    result = selector("SCA_BUZZ", func_details, 12, 8)
    assert result is None or result is False