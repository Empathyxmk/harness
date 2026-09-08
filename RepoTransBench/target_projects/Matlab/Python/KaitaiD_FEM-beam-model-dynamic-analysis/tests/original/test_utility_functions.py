import numpy as np
import pytest
from src.fem.utility import integrationpoints, integrationweights, shapefunctions, shapefunctionderivs

def test_integrationpoints_n2():
    pts = integrationpoints(2)
    pts_expected = np.array([-1/np.sqrt(3), 1/np.sqrt(3)])
    assert np.linalg.norm(pts - pts_expected) <= 1e-12

def test_integrationweights_n2():
    wts = integrationweights(2)
    wts_expected = np.array([1.0, 1.0])
    assert np.linalg.norm(wts - wts_expected) <= 1e-12

def test_shapefunctions_xi0():
    N = shapefunctions(0)
    N_expected = np.array([0.5, 0.5])
    assert np.linalg.norm(N - N_expected) <= 1e-12

def test_shapefunctionderivs_xi0():
    dN = shapefunctionderivs(0)
    dN_expected = np.array([-0.5, 0.5])
    assert np.linalg.norm(dN - dN_expected) <= 1e-12