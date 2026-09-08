import pytest
import numpy as np
from src.genann import *

def test_xor():
    ann = genann_init(2, 1, 2, 1)
    ann.activation_hidden = genann_act_threshold
    ann.activation_output = genann_act_threshold

    assert ann.total_weights == 9

    # Assign weights for XOR as in the original C code
    ann.weight[0] = 0.5
    ann.weight[1] = 1
    ann.weight[2] = 1

    ann.weight[3] = 1
    ann.weight[4] = 1
    ann.weight[5] = 1

    ann.weight[6] = 0.5
    ann.weight[7] = 1
    ann.weight[8] = -1

    input = [[0,0],[0,1],[1,0],[1,1]]
    output = [0,1,1,0]
    for i in range(4):
        assert np.isclose(genann_run(ann, input[i]), output[i], atol=0.001)