import pytest
import numpy as np
from src.genann import *

def test_basic():
    ann = genann_init(1, 0, 0, 1)

    assert ann.total_weights == 2
    a = 0
    ann.weight[0] = 0
    ann.weight[1] = 0
    r = genann_run(ann, [a])
    assert np.isclose(r, 0.5, atol=0.001)
    a = 1
    assert np.isclose(genann_run(ann, [a]), 0.5, atol=0.001)
    a = 11
    assert np.isclose(genann_run(ann, [a]), 0.5, atol=0.001)
    a = 1
    ann.weight[0] = 1
    ann.weight[1] = 1
    assert np.isclose(genann_run(ann, [a]), 0.5, atol=0.001)
    a = 10
    ann.weight[0] = 1
    ann.weight[1] = 1
    assert np.isclose(genann_run(ann, [a]), 1.0, atol=0.001)
    a = -10
    assert np.isclose(genann_run(ann, [a]), 0.0, atol=0.001)