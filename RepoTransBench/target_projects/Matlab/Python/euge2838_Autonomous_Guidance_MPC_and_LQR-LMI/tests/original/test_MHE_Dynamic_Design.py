import pytest
import numpy as np

# Dummy definition only for structure.
def MHE_Dynamic_Design(parameters):
    # parameters: dict with 'Q' and 'R'
    Q = parameters['Q']
    R = parameters['R']
    return {
        'state_estimate': np.zeros((Q.shape[0], 1)),
        'covariance': np.eye(Q.shape[0])
    }

def test_MHE_Dynamic_Design():
    # Example input; shape matches Matlab example.
    parameters = {'Q': np.eye(2), 'R': np.eye(2)}
    result = MHE_Dynamic_Design(parameters)

    assert 'state_estimate' in result
    assert 'covariance' in result
    assert result['state_estimate'].shape[0] == 2
    assert result['covariance'].shape == (2, 2)