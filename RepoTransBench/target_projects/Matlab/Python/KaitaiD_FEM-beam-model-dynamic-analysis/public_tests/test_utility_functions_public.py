import numpy as np
import pytest
from src.fem.utility import integrationpoints, integrationweights, shapefunctions, shapefunctionderivs

def test_integrationpoints_n3_public():
    pts = integrationpoints(3)
    pts_expected = np.array([-np.sqrt(3/5), 0.0, np.sqrt(3/5)])
    assert np.linalg.norm(pts - pts_expected) <= 1e-12

def test_integrationweights_n3_public():
    wts = integrationweights(3)
    wts_expected = np.array([5/9, 8/9, 5/9])
    assert np.linalg.norm(wts - wts_expected) <= 1e-12

def test_shapefunctions_xi1_public():
    N = shapefunctions(1)
    N_expected = np.array([0.0, 1.0])
    assert np.linalg.norm(N - N_expected) <= 1e-12

def test_shapefunctionderivs_xim1_public():
    dN = shapefunctionderivs(-1)
    dN_expected = np.array([-0.5, 0.5])
    assert np.linalg.norm(dN - dN_expected) <= 1e-12