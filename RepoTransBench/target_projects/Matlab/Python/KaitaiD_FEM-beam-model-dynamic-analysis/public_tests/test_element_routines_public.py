import numpy as np
import pytest
from src.fem.element import elstif, elmass, eldload

def test_elstif_public():
    # ==== Test elstif: Different E, A, x1, x2 ====
    E = 1.2e4
    A = 0.7
    x1 = 1.1
    x2 = 3.6
    ke = elstif(E, A, [x1, x2])
    exp_ke = E*A/(x2-x1) * np.array([[1, -1], [-1, 1]])
    assert np.linalg.norm(ke - exp_ke, ord='fro') < 1e-10

def test_elmass_public():
    # ==== Test elmass: Different rho, A, x1, x2 ====
    rho = 2.5
    A = 0.42
    x1 = -2.0
    x2 = 0.0
    me = elmass(rho, A, [x1, x2])
    le = x2 - x1
    exp_me = rho*A*le/6 * np.array([[2, 1], [1, 2]])
    assert np.linalg.norm(me - exp_me, ord='fro') < 1e-10

def test_eldload_public():
    # ==== Test eldload: Different q, x1, x2 ====
    q = -7.8
    x1 = 3.0
    x2 = 3.5
    fe = eldload(q, [x1, x2])
    le = x2 - x1
    exp_fe = q*le/2 * np.array([[1], [1]])
    assert np.linalg.norm(fe - exp_fe) < 1e-10