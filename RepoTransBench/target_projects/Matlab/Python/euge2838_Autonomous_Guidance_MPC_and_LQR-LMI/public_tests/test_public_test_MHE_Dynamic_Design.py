import pytest
import numpy as np

def MHE_Dynamic_Design(parameters):
    Q = np.array(parameters['Q'])
    R = np.array(parameters['R'])
    state_estimate = np.zeros((Q.shape[0], 1))
    covariance = np.eye(Q.shape[0])
    return {
        'state_estimate': state_estimate,
        'covariance': covariance
    }

def test_public_test_MHE_Dynamic_Design():
    parameters = {
        'Q': np.array([[3, 1], [1, 2]]),
        'R': np.array([[2, 0], [0, 2]])
    }
    result = MHE_Dynamic_Design(parameters)

    assert 'state_estimate' in result
    assert 'covariance' in result
    assert result['state_estimate'].shape[0] == 2
    assert result['covariance'].shape == (2, 2)