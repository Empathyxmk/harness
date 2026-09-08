import numpy as np
from src.izougend_mcmcda.kalman import kalman_step

def test_kalman_public_basic_shape():
    x0 = np.array([1, -1, 0.5, 2])
    P0 = np.eye(4) * 0.5
    F = np.eye(4) + 0.1 * np.array([[0,1,0,0],[0,0,0,0],[0,0,0,1],[0,0,0,0]])
    Q = 0.05 * np.eye(4)
    H = np.array([[1,0,1,0],[0,1,0,1]])
    R = np.diag([0.3, 0.4])
    z = np.array([1.8, -0.4])

    x_pred, P_pred, x_upd, P_upd = kalman_step(x0, P0, F, Q, H, R, z)
    assert x_pred.shape == (4,)
    assert x_upd.shape == (4,)
    assert P_pred.shape == (4,4)
    assert P_upd.shape == (4,4)

def test_kalman_public_additional():
    x0 = np.array([1, -1, 0.5, 2])
    P0 = np.eye(4) * 0.5
    F = np.eye(4) + 0.1 * np.array([[0,1,0,0],[0,0,0,0],[0,0,0,1],[0,0,0,0]])
    H = np.array([[1,0,1,0],[0,1,0,1]])
    R = np.diag([0.3, 0.4])
    z = np.array([5.2, -2.7])
    Q = np.eye(4) * 0.1
    x_pred2, P_pred2, x_upd2, P_upd2 = kalman_step(x0, P0, F, Q, H, R, z)
    assert abs(x_upd2[0] - z[0]) < 5