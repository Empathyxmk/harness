import numpy as np
import pytest

class Distrib:
    def __init__(self):
        self.max = 0
        self.std_dev = 2.7
        self.table = None

def Sample(d):
    return int(np.round(np.random.normal(d.max, d.std_dev)))

def test_sample_with_different_stddev():
    d = Distrib()
    x = Sample(d)
    assert -32 <= x <= 32