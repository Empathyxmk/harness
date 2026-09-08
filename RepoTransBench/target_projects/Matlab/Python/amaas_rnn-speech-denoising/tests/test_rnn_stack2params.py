import numpy as np
from src.rnn_stack2params import rnn_stack2params, rnn_params2stack

def test_rnn_stack2params_rnn_params2stack_roundtrip():
    stack = {'W': np.random.rand(2,2), 'b': np.random.rand(2,1)}
    params = rnn_stack2params(stack)
    stack2 = rnn_params2stack(params, {'W': np.zeros((2,2)), 'b': np.zeros((2,1))})
    assert 'W' in stack2 and 'b' in stack2
    assert stack2['W'].shape == (2,2)