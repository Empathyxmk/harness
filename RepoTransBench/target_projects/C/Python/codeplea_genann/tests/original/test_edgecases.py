from src.genann import *
import numpy as np
import tempfile
import os

def test_invalid_inits():
    ann = genann_init(0, 1, 2, 1)
    assert ann is None
    ann = genann_init(2, -1, 2, 1)
    assert ann is None
    ann = genann_init(2, 1, 2, 0)
    assert ann is None
    ann = genann_init(2, 1, 0, 1)
    assert ann is None

def test_copy_random_free():
    ann = genann_init(2, 1, 2, 1)
    assert ann is not None
    copy = genann_copy(ann)
    assert copy is not None
    genann_randomize(ann)
    rand_changed = np.any(ann.weight != copy.weight)
    assert rand_changed

def test_activations():
    ann = type('FakeAnn', (object,), {})()
    ann.activation_hidden = genann_act_sigmoid
    ann.activation_output = genann_act_sigmoid
    t = genann_act_sigmoid(ann, -100)
    assert t >= 0 and t < 0.01
    t = genann_act_sigmoid(ann, 100)
    assert t > 0.99 and t <= 1.0
    val0 = genann_act_sigmoid(ann, 0)
    assert val0 > 0 and val0 < 1
    t = genann_act_threshold(ann, -1)
    assert int(t) == 0
    t = genann_act_threshold(ann, +1)
    assert int(t) == 1
    t = genann_act_linear(ann, 5)
    assert int(t) == 5

def test_file_io(tmp_path):
    ann = genann_init(2, 1, 2, 1)
    p = tmp_path / "test.ann"
    with open(p, "wb") as f:
        genann_write(ann, f)
    with open(p, "rb") as f:
        read_ann = genann_read(f)
    assert read_ann is not None
    genann_free(ann)
    genann_free(read_ann)
    # Try to read a corrupt file
    p2 = tmp_path / "test_broken.ann"
    with open(p2, "wb") as f:
        f.write(b"corrupt-data")
    with open(p2, "rb") as f:
        broken = genann_read(f)
    assert broken is None