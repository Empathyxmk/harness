import numpy as np
import warnings
import pytest
from src.kaenchan_robust_elm_irls.robust_func import robust_func

def test_robust_func():
    tol = 1e-9

    # Test Case 1: functype 'l1'
    z = np.array([-2, -1, 0, 1, 2])
    # rho
    expected_rho = np.array([2, 1, 0, 1, 2])
    actual_rho = robust_func(z, 'l1', 'rho')
    assert np.all(np.abs(actual_rho - expected_rho) < tol), 'L1 rho test failed'
    # psi
    expected_psi = np.array([-1, -1, 0, 1, 1])
    actual_psi = robust_func(z, 'l1', 'psi')
    assert np.all(np.abs(actual_psi - expected_psi) < tol), 'L1 psi test failed'
    # wgt
    expected_wgt = np.array([1/2, 1, 1/0.000001, 1, 1/2])
    actual_wgt = robust_func(z, 'l1', 'wgt')
    assert np.all(np.abs(actual_wgt - expected_wgt) < tol), 'L1 wgt test failed'

    # Test Case 2: functype 'huber'
    delta = 1.5
    z = np.array([-2, -1, 0, 1, 1.5, 2])
    # rho
    expected_rho_huber = np.zeros(z.shape)
    k_mask = np.abs(z) < delta
    expected_rho_huber[k_mask] = 0.5 * z[k_mask] ** 2
    expected_rho_huber[~k_mask] = delta * (np.abs(z[~k_mask]) - delta / 2)
    actual_rho_huber = robust_func(z, 'huber', 'rho', delta)
    assert np.all(np.abs(actual_rho_huber - expected_rho_huber) < tol), 'Huber rho test failed'
    # psi
    expected_psi_huber = np.zeros(z.shape)
    k_mask = np.abs(z) < delta
    expected_psi_huber[k_mask] = z[k_mask]
    expected_psi_huber[~k_mask] = delta * np.sign(z[~k_mask])
    actual_psi_huber = robust_func(z, 'huber', 'psi', delta)
    assert np.all(np.abs(actual_psi_huber - expected_psi_huber) < tol), 'Huber psi test failed'
    # wgt
    expected_wgt_huber = np.minimum(1, delta / np.abs(z))
    expected_wgt_huber[np.isinf(expected_wgt_huber)] = 1
    actual_wgt_huber = robust_func(z, 'huber', 'wgt', delta)
    assert np.all(np.abs(actual_wgt_huber - expected_wgt_huber) < tol), 'Huber wgt test failed'

    # Test Case 3: functype 'bisquare'
    delta = 2.0
    z = np.array([-3, -1, 0, 1, 2, 3])
    # rho
    expected_rho_bisquare = np.zeros(z.shape)
    k_mask = np.abs(z) < delta
    expected_rho_bisquare[k_mask] = 1/6 * delta * delta * (1 - (1 - (z[k_mask]/delta) ** 2) ** 3)
    expected_rho_bisquare[~k_mask] = 1/6 * delta * delta
    actual_rho_bisquare = robust_func(z, 'bisquare', 'rho', delta)
    assert np.all(np.abs(actual_rho_bisquare - expected_rho_bisquare) < tol), 'Bisquare rho test failed'
    # psi
    expected_psi_bisquare = np.zeros(z.shape)
    k_mask = np.abs(z) < delta
    expected_psi_bisquare[k_mask] = z[k_mask] * (1 - (z[k_mask]/delta) ** 2) ** 2
    actual_psi_bisquare = robust_func(z, 'bisquare', 'psi', delta)
    assert np.all(np.abs(actual_psi_bisquare - expected_psi_bisquare) < tol), 'Bisquare psi test failed'
    # wgt
    expected_wgt_bisquare = np.zeros(z.shape)
    k_mask = np.abs(z) < delta
    expected_wgt_bisquare[k_mask] = (1 - (z[k_mask]/delta) ** 2) ** 2
    actual_wgt_bisquare = robust_func(z, 'bisquare', 'wgt', delta)
    assert np.all(np.abs(actual_wgt_bisquare - expected_wgt_bisquare) < tol), 'Bisquare wgt test failed'

    # Test Case 4: functype 'cauchy'
    delta = 2.5
    z = np.array([-5, -2.5, 0, 2.5, 5])
    expected_rho_cauchy = 0.5 * np.log(1 + (z/delta) ** 2)
    actual_rho_cauchy = robust_func(z, 'cauchy', 'rho', delta)
    assert np.all(np.abs(actual_rho_cauchy - expected_rho_cauchy) < tol), 'Cauchy rho test failed'
    expected_psi_cauchy = z / (1 + (z/delta) ** 2)
    actual_psi_cauchy = robust_func(z, 'cauchy', 'psi', delta)
    assert np.all(np.abs(actual_psi_cauchy - expected_psi_cauchy) < tol), 'Cauchy psi test failed'
    expected_wgt_cauchy = 1 / (1 + (z/delta) ** 2)
    actual_wgt_cauchy = robust_func(z, 'cauchy', 'wgt', delta)
    assert np.all(np.abs(actual_wgt_cauchy - expected_wgt_cauchy) < tol), 'Cauchy wgt test failed'

    # Test Case 5: functype 'welsch'
    delta = 3.0
    z = np.array([-6, -3, 0, 3, 6])
    expected_rho_welsch = 1/delta/delta * np.exp(-0.5 * (z/delta) ** 2)
    actual_rho_welsch = robust_func(z, 'welsch', 'rho', delta)
    assert np.all(np.abs(actual_rho_welsch - expected_rho_welsch) < tol), 'Welsch rho test failed'
    expected_psi_welsch = z * np.exp(-0.5 * (z/delta) ** 2)
    actual_psi_welsch = robust_func(z, 'welsch', 'psi', delta)
    assert np.all(np.abs(actual_psi_welsch - expected_psi_welsch) < tol), 'Welsch psi test failed'
    expected_wgt_welsch = np.exp(-0.5 * (z/delta) ** 2)
    actual_wgt_welsch = robust_func(z, 'welsch', 'wgt', delta)
    assert np.all(np.abs(actual_wgt_welsch - expected_wgt_welsch) < tol), 'Welsch wgt test failed'

    # Test Case 6: functype 'ggw'
    a = 1.0
    b = 2.0
    c = 1.0
    z = np.array([-2, 0, 0.5, 1, 1.5, 2])
    expected_rho_ggw = np.ones(z.shape)
    actual_rho_ggw = robust_func(z, 'ggw', 'rho', a, b, c)
    assert np.all(np.abs(actual_rho_ggw - expected_rho_ggw) < tol), 'GGW rho test failed'
    expected_psi_ggw = np.zeros(z.shape)
    c_mask = np.abs(z) <= c
    expected_psi_ggw[c_mask] = z[c_mask]
    expected_psi_ggw[~c_mask] = z[~c_mask] * np.exp(-0.5 * ((z[~c_mask] - c) ** b))
    actual_psi_ggw = robust_func(z, 'ggw', 'psi', a, b, c)
    assert np.all(np.abs(actual_psi_ggw - expected_psi_ggw) < tol), 'GGW psi test failed'
    expected_wgt_ggw = np.zeros(z.shape)
    expected_wgt_ggw[c_mask] = 1
    expected_wgt_ggw[~c_mask] = np.exp(-0.5 * ((z[~c_mask] - c) ** b))
    actual_wgt_ggw = robust_func(z, 'ggw', 'wgt', a, b, c)
    assert np.all(np.abs(actual_wgt_ggw - expected_wgt_ggw) < tol), 'GGW wgt test failed'

    # Test Case 7: Invalid outtype, should warn
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        robust_func(1, 'l1', 'invalid')
        assert any('error outtype' in str(x.message) for x in w), "Warning for invalid outtype not found for l1"

    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        robust_func(1, 'huber', 'invalid', 1)
        assert any('error outtype' in str(x.message) for x in w), "Warning for invalid outtype not found for huber"

    # Test Case 8: Invalid functype, should warn
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        robust_func(1, 'invalid_func', 'rho')
        assert any('error functype' in str(x.message) for x in w), "Warning for invalid functype not found"