import numpy as np
from src.multipolyregress import MultiPolyRegress

def test_simple_linear_regression_public():
    # Public Test 1: Simple linear regression with different data
    np.random.seed(42)
    X = np.arange(1, 6).reshape(-1, 1)
    Y = 4 * X.flatten() + 3 + np.random.randn(5) * 0.1  # y = 4x + 3 + noise
    degree = 1
    mpr = MultiPolyRegress(X, Y, degree)
    Y_pred = mpr.Coeff[0] + mpr.Coeff[1]*X.flatten()
    assert np.all(np.abs(Y - Y_pred) < 1), "Public Test 1 failed: Fit did not match expected within tolerance."

def test_quadratic_fit_public():
    # Public Test 2: Quadratic fit with another set
    np.random.seed(43)
    X = np.linspace(1, 10, 10).reshape(-1, 1)
    Y = 2 * X.flatten()**2 - 3*X.flatten() + 5 + np.random.randn(10) * 0.2 # y = 2x^2 - 3x + 5 + noise
    degree = 2
    mpr2 = MultiPolyRegress(X, Y, degree)
    Y_pred2 = mpr2.Coeff[0] + mpr2.Coeff[1]*X.flatten() + mpr2.Coeff[2]*X.flatten()**2
    assert np.all(np.abs(Y - Y_pred2) < 2), "Public Test 2 failed: Quadratic fit did not match expected within tolerance."

def test_multivariate_input_public():
    # Public Test 3: Multivariate input, different numbers
    np.random.seed(44)
    X = np.array([
        [1, 3],
        [2, 4],
        [3, 5],
        [4, 6],
        [5, 7]
    ])
    Y = 1 + 2 * X[:, 0] + 3 * X[:, 1] + np.random.randn(5) * 0.1  # y = 1 + 2*x1 + 3*x2 + noise
    degree = 1
    mpr3 = MultiPolyRegress(X, Y, degree)
    Y_pred3 = mpr3.Coeff[0] + mpr3.Coeff[1]*X[:,0] + mpr3.Coeff[2]*X[:,1]
    assert np.all(np.abs(Y - Y_pred3) < 1), "Public Test 3 failed: Multivariate fit did not match expected within tolerance."