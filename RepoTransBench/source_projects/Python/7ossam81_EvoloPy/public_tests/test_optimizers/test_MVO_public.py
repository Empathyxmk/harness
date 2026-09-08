import pytest
from EvoloPy.optimizer import selector

def test_mvo_public_valid():
    func_details = ['F4', -300, 300, 12]
    popSize = 6
    Iter = 4
    algo = selector("MVO", func_details, popSize, Iter)
    assert hasattr(algo, 'fitness') or hasattr(algo, 'convergence')

def test_mvo_public_invalid():
    func_details = ['F4', -300, 300, 12]
    # Invalid algorithm name for negative branch
    result = selector("MVO_FAKE", func_details, 6, 4)
    assert result is None or result is False