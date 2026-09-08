import tempfile
import numpy as np
from src.genann import *

def test_persist(tmp_path):
    first = genann_init(1000, 5, 50, 10)
    path = tmp_path / "persist.ann"
    with open(path, "wb") as f:
        genann_write(first, f)

    with open(path, "rb") as f:
        second = genann_read(f)
    assert first.inputs == second.inputs
    assert first.hidden_layers == second.hidden_layers
    assert first.hidden == second.hidden
    assert first.outputs == second.outputs
    assert first.total_weights == second.total_weights
    for i in range(first.total_weights):
        assert first.weight[i] == second.weight[i]