import numpy as np
import pytest
from src.fem.element import elstif, elmass, eldload

def test_elstif():
    E = 2e5
    A = 2.0
    x1 = 0
    x2 = 2.0
    ke = elstif(E, A, [x1, x2])
    exp_ke = E*A/(x2-x1) * np.array([[1, -1], [-1, 1]])
    assert np.linalg.norm(ke - exp_ke, ord='fro') < 1e-10

def test_elmass():
    rho = 0.75
    A = 1.5
    x1 = 0.5
    x2 = 1.5
    me = elmass(rho, A, [x1, x2])
    le = x2 - x1
    exp_me = rho*A*le/6 * np.array([[2, 1], [1, 2]])
    assert np.linalg.norm(me - exp_me, ord='fro') < 1e-10

def test_eldload():
    q = 4.5
    x1 = 5.0
    x2 = 8.0
    fe = eldload(q, [x1, x2])
    le = x2 - x1
    exp_fe = q*le/2 * np.array([[1], [1]])
    assert np.linalg.norm(fe - exp_fe) < 1e-10