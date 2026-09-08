import numpy as np
from src.rnn_stack2params import rnn_stack2params

def test_rnn_stack2params_empty_stack():
    w = rnn_stack2params({})
    assert w is None or isinstance(w, np.ndarray)

def test_rnn_stack2params_minimal_input():
    stack = {'w': np.random.randn(2,2), 'b': [], 'U': np.random.randn(2,2)}
    w = rnn_stack2params(stack)
    assert isinstance(w, np.ndarray)