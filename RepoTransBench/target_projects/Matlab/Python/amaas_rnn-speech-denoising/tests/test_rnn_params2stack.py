import pytest
from src.rnn_params2stack import rnn_params2stack

def test_rnn_params2stack_normal_case():
    params = list(range(1, 15))
    netConfig = {'size': [2,3,2], 'hActType': [1,2]}
    stack = rnn_params2stack(params, netConfig)
    assert 'layers' in stack
    assert len(stack['layers']) == 2

def test_rnn_params2stack_too_few_params():
    params = list(range(1,5))
    netConfig = {'size': [2,3,2], 'hActType': [1,2]}
    with pytest.raises(Exception):
        rnn_params2stack(params, netConfig)