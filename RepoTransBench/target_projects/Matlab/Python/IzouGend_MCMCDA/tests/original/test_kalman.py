import pytest
import numpy as np
from src.izougend_mcmcda.kalman import kalman

@pytest.fixture
def kalman_globals():
    Ts = 1
    sigmaW = 0.02
    sigmaV = 0.01
    P0 = np.eye(6) * 100
    A = np.array([
        [1, Ts, 0, 0, 0, 0],
        [0, 1,  0, 0, 0, 0],
        [0, 0,  1, Ts,0, 0],
        [0, 0,  0, 1, 0, 0],
        [0, 0,  0, 0, 1, Ts],
        [0, 0,  0, 0, 0, 1]
    ])
    C = np.array([
        [1, 0, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 1, 0]
    ])
    Q = np.eye(6) * sigmaW
    R = np.eye(3) * sigmaV
    return P0, A, C, Q, R

def test_kalman_case1_basic(kalman_globals):
    P0, A, C, Q, R = kalman_globals
    # y shape: (steps, 3)
    y1 = np.tile(np.array([[10, 20, 30]]), (5, 1))
    xhat_out1, Pout1 = kalman(y1, 1, y1.shape[0], P0, A, C, Q, R)
    assert xhat_out1.shape[1] == y1.shape[0]+1
    assert Pout1.shape[2] == y1.shape[0]
    assert np.any(xhat_out1 != 0)
    assert np.all(np.isfinite(xhat_out1))
    assert np.all(np.isfinite(Pout1))

def test_kalman_case2_nan(kalman_globals):
    P0, A, C, Q, R = kalman_globals
    y2 = np.array([
        [10, np.nan, 30],
        [15, 25, np.nan],
        [np.nan, np.nan, np.nan],
        [40, 50, 60],
    ])
    xhat_out2, Pout2 = kalman(y2, 1, y2.shape[0], P0, A, C, Q, R)
    assert xhat_out2.shape[1] == y2.shape[0]+1
    assert np.all(np.isfinite(xhat_out2))
    assert np.all(np.isfinite(Pout2))

def test_kalman_case3_single_iter(kalman_globals):
    P0, A, C, Q, R = kalman_globals
    y3 = np.tile(np.array([[5, 10, 15]]), (1, 1))
    xhat_out3, Pout3 = kalman(y3, 1, 1, P0, A, C, Q, R)
    assert xhat_out3.shape[1] == 2
    assert Pout3.shape[2] == 1