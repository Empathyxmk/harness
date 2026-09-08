import pytest
import numpy as np
from src.genann import *

def test_train_xor():
    input_data = np.array([[0,0],[0,1],[1,0],[1,1]])
    output = [0,1,1,0]
    ann = genann_init(2, 1, 2, 1)
    for i in range(500):
        for j in range(4):
            genann_train(ann, input_data[j], [output[j]], 3)
    ann.activation_output = genann_act_threshold
    for i in range(4):
        assert np.isclose(genann_run(ann, input_data[i]), output[i], atol=0.001)