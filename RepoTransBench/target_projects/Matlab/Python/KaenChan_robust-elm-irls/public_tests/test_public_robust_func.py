import numpy as np
import pytest
from src.kaenchan_robust_elm_irls.robust_func import robust_func

# Uses separate functions to mimic Matlab 'functiontests'
def test_huber():
    y = np.array([-3.2, -1.0, 0.0, 1.0, 2.4, 5.5])
    c = 1.5
    # Calculate, matching Matlab logic
    g = robust_func(y, 'huber', 'rho', c)
    exp = np.array([2.55, 0.5, 0, 0.5, 1.7, 5.25])
    np.testing.assert_allclose(g, exp, atol=1e-10)

def test_bisquare():
    y = np.array([-2, -0.8, 0, 0.9, 1.7, 2.5])
    c = 1.25
    g = robust_func(y, 'bisquare', 'rho', c)
    # Bisquare: = (abs(y) < c) .* (c^2/6 * (1-(1-(y/c).^2).^3)) + (abs(y) >= c) .* (c^2/6)
    l = np.abs(y) < c
    bsq = np.zeros_like(y, dtype=float)
    bsq[l] = (c ** 2) / 6 * (1 - (1 - (y[l] / c) ** 2) ** 3)
    bsq[~l] = (c ** 2) / 6
    np.testing.assert_allclose(g, bsq, atol=1e-10)

def test_fair():
    y = np.array([-4, -2, 0, 2, 3.5])
    c = 0.7
    g = robust_func(y, 'fair', 'rho', c)
    expected = c ** 2 * (np.abs(y) / c - np.log(1 + np.abs(y) / c))
    np.testing.assert_allclose(g, expected, atol=1e-10)

def test_cauchy():
    y = np.array([-1.5, -0.5, 0, 0.5, 1.5])
    c = 1.1
    g = robust_func(y, 'cauchy', 'rho', c)
    expected = (c ** 2) / 2 * np.log(1 + (y / c) ** 2)
    np.testing.assert_allclose(g, expected, atol=1e-10)

def test_welsch():
    y = np.array([-2.5, -0.9, 0, 1, 2.0])
    c = 1.8
    g = robust_func(y, 'welsch', 'rho', c)
    expected = (c ** 2) / 2 * (1 - np.exp(-(y / c) ** 2))
    np.testing.assert_allclose(g, expected, atol=1e-10)

def test_default_to_l2():
    y = np.array([1, -2, 0.5])
    g = robust_func(y, 'doesnotexist', 'rho', 1.0)
    expected = y ** 2
    np.testing.assert_allclose(g, expected, atol=1e-10)