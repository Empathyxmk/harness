import numpy as np
from src.genann import *

def test_sigmoid():
    i = -20
    maxv = 20
    d = 0.0001
    while i < maxv:
        x = genann_act_sigmoid(None, i)
        y = genann_act_sigmoid_cached(None, i)
        assert np.isclose(x, y, atol=0.001)
        i += d