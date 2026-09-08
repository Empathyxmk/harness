import numpy as np
import pytest
from src.fem.material import materialstiffness

def test_materialstiffness_strain():
    E = 210000
    nu = 0.3
    C = materialstiffness('strain', E, nu)
    C_expected = E/(1+nu)/(1-2*nu) * np.array([
        [1-nu, nu, 0],
        [nu, 1-nu, 0],
        [0, 0, (1-2*nu)/2]
    ])
    assert np.linalg.norm(C - C_expected, ord='fro') < 1e-10

def test_materialstiffness_stress():
    E2 = 70000
    nu2 = 0.33
    C2 = materialstiffness('stress', E2, nu2)
    C2_expected = E2/(1-nu2**2) * np.array([
        [1, nu2, 0],
        [nu2, 1, 0],
        [0, 0, (1-nu2)/2]
    ])
    assert np.linalg.norm(C2 - C2_expected, ord='fro') < 1e-10

def test_materialstiffness_beam():
    E3 = 123e3
    C3 = materialstiffness('beam', E3)
    assert abs(C3 - E3) < 1e-10

def test_materialstiffness_truss():
    E4 = 3.2e4
    C4 = materialstiffness('truss', E4)
    assert abs(C4 - E4) < 1e-10