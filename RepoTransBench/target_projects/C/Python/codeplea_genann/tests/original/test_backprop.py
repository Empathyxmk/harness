import pytest
import numpy as np
from src.genann import *

def test_backprop():
    ann = genann_init(1, 0, 0, 1)
    input_ = 0.5
    output = 1.0

    first_try = genann_run(ann, [input_])
    genann_train(ann, [input_], [output], .5)
    second_try = genann_run(ann, [input_])
    assert abs(first_try - output) > abs(second_try - output)