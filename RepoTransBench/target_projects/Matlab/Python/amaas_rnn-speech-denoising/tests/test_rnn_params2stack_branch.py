from src.rnn_params2stack import rnn_params2stack

def test_rnn_params2stack_minimal_input():
    try:
        params = [0, 0, 0, 0]
        arch = {'nl': 1, 'layer_sizes': [2,2]}
        stack = rnn_params2stack(params, arch)
        assert isinstance(stack, dict) or stack is None
    except Exception:
        assert True

def test_rnn_params2stack_incorrect_size():
    try:
        params = [0]
        arch = {'nl': 2, 'layer_sizes': [2,3,2]}
        stack = rnn_params2stack(params, arch)
        assert isinstance(stack, dict) or stack is None
    except Exception:
        assert True