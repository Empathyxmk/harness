import numpy as np
import pytest
from src.fem.material import materialstiffness

def test_materialstiffness_strain_public():
    # Plane strain test: Different E, nu
    E = 325000
    nu = 0.27
    C = materialstiffness('strain', E, nu)
    C_expected = E/(1+nu)/(1-2*nu) * np.array([
        [1-nu, nu, 0],
        [nu, 1-nu, 0],
        [0, 0, (1-2*nu)/2]
    ])
    assert np.linalg.norm(C - C_expected, ord='fro') < 1e-10

def test_materialstiffness_stress_public():
    # Plane stress test: Different E, nu
    E2 = 95000
    nu2 = 0.18
    C2 = materialstiffness('stress', E2, nu2)
    C2_expected = E2/(1-nu2**2) * np.array([
        [1, nu2, 0],
        [nu2, 1, 0],
        [0, 0, (1-nu2)/2]
    ])
    assert np.linalg.norm(C2 - C2_expected, ord='fro') < 1e-10

def test_materialstiffness_beam_public():
    # Beam case: Different E
    E3 = 2.21e5
    C3 = materialstiffness('beam', E3)
    assert abs(C3 - E3) < 1e-10

def test_materialstiffness_truss_public():
    # Truss case: Different E
    E4 = 1.84e3
    C4 = materialstiffness('truss', E4)
    assert abs(C4 - E4) < 1e-10