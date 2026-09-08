import pytest
import numpy as np
from src.genann import *
import time

def test_public_xor_and():
    # GENANN public test: Train on AND function.
    np.random.seed(int(time.time()))
    input_data = np.array([[0,0],[0,1],[1,0],[1,1]])
    output = [0,0,0,1]
    ann = genann_init(2, 1, 2, 1)
    for i in range(500):
        for j in range(4):
            genann_train(ann, input_data[j], [output[j]], 2.5)
    for i in range(4):
        print(f"Output for {input_data[i]} is {genann_run(ann, input_data[i])}.")
    genann_free(ann)