import pytest
from EvoloPy.optimizer import selector

def test_jaya_public_valid():
    func_details = ['F11', -120, 120, 7]
    popSize = 4
    Iter = 12
    algo = selector("JAYA", func_details, popSize, Iter)
    assert hasattr(algo, 'fitness') or hasattr(algo, 'convergence')

def test_jaya_public_invalid():
    func_details = ['F11', -120, 120, 7]
    result = selector("JAYA_NOALG", func_details, 4, 12)
    assert result is None or result is False