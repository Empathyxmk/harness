import numpy as np
from ukfmanifold.quaternions import qdecomp, qnorm

def test_angle_axis_basic():
    # q = [axis*sin(theta/2), cos(theta/2)]
    axis = np.array([1,0,0])
    angle = np.pi / 2
    q = np.hstack([axis*np.sin(angle/2), np.cos(angle/2)])
    phi, n = qdecomp(q)
    assert np.isclose(phi, angle)
    assert np.allclose(n, axis)