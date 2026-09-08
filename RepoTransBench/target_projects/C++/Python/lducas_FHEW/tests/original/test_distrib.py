import numpy as np
import pytest

class Distrib:
    def __init__(self):
        self.max = 0
        self.std_dev = 1.0
        self.table = None
        self.offset = 0

def Sample(d):
    # Simulate sampling
    if d.table is not None:
        # Table as cumulative distribution
        p = np.random.uniform()
        for idx, prob in enumerate(d.table):
            if p < prob:
                return idx - d.offset
        return len(d.table) - 1 - d.offset
    else:
        return int(np.round(np.random.normal(d.max, d.std_dev)))

def test_sample_small_std_dev():
    d = Distrib()
    d.max = 0
    d.std_dev = 2
    np.random.seed(42)
    samples = [Sample(d) for _ in range(100)]
    mean = np.mean(samples)
    assert -2 < mean < 2

def test_sample_large_std_dev():
    d = Distrib()
    d.max = 0
    d.std_dev = 1000
    np.random.seed(123)
    s = Sample(d)
    assert abs(s) < 9000

def test_sample_tabular():
    d = Distrib()
    d.max = 3
    d.table = [0.3, 0.6, 1.0]
    d.offset = 1
    np.random.seed(1)
    val = Sample(d)
    assert -1 <= val <= 1