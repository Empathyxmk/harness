from src.genann import *

def test_copy():
    first = genann_init(1000, 5, 50, 10)
    second = genann_copy(first)
    assert first.inputs == second.inputs
    assert first.hidden_layers == second.hidden_layers
    assert first.hidden == second.hidden
    assert first.outputs == second.outputs
    assert first.total_weights == second.total_weights
    for i in range(first.total_weights):
        assert first.weight[i] == second.weight[i]