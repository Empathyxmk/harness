import pytest
import numpy as np
from src.genann import *

def test_public_edgecases():
    # Construct with more neurons and layers than in original edge case
    ann = genann_init(3, 2, 4, 2)
    assert ann is not None

    input1 = [0.0, 1.0, -1.0]
    out1 = genann_run(ann, input1)
    assert out1 is not None

    train_in = [0.5, 0.2, 0.8]
    train_out = [0.9, 0.1]
    genann_train(ann, train_in, train_out, 1.9)
    out2 = genann_run(ann, train_in)
    assert out2 is not None

    # Output for sanity (float values due to neural properties, not equality)
    print(f"Sanity: output1 = {out1}, output2 = {out2}")

    assert ann.inputs == 3
    assert ann.outputs == 2
    assert ann.hidden_layers == 2
    assert ann.hidden == 4

    genann_free(ann)

    # Freeing already freed network (should handle safely)
    genann_free(None)

    # Passing None as input to run, should not crash, returns output buffer
    ann = genann_init(1,0,0,1)
    o = genann_run(ann, None)
    assert o is not None
    genann_free(ann)