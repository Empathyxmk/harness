import pytest
import numpy as np
from src.sp import array_pattern

def test_uniform_array():
    pat = array_pattern(8, 0, 0, np.ones(8))
    assert len(pat) == 361

def test_edge_cases():
    pat = array_pattern(1, 0, 0, 1)
    assert len(pat) > 0
    pat2 = array_pattern(4, 90, 0, np.ones(4))
    assert len(pat2) == 361

def test_complex_weights():
    pat = array_pattern(4, 0, 0, [1, 1j, 1, -1j])
    assert len(pat) == 361