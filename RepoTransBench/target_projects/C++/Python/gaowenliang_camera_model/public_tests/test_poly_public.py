import pytest
import numpy as np

def public_fit_test():
    # Different data: quadratic curve with noise
    xx = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11], dtype=float)
    out = np.array([1.0, 3.95, 8.1, 13.2, 20.1, 28.4, 38.2, 48.9, 62.2, 77.1, 92.8, 110.2], dtype=float)
    # We'll fit a 2nd order polynomial y = a*x^2 + b*x + c
    # numpy polyfit returns coefficients in decreasing order
    coeff = np.polyfit(xx, out, 2)
    poly = np.poly1d(coeff)
    fit_values = poly(xx)
    # Quick check: the poly should be close to data (allow <= 2.0 absolute error)
    for xi, actual, predicted in zip(xx, out, fit_values):
        assert abs(actual - predicted) <= 2.0, f"Fit error too large at x={xi}: got {predicted} expected {actual}"

def public_test_poly():
    # f(x) = 5 - 2x + 0.5x^2 + 0.1x^3
    coeffs = np.array([5, -2, 0.5, 0.1], dtype=float)
    # numpy needs coefficients as [a0, a1, a2, ...], highest degree first
    # So for cubic: a3, a2, a1, a0
    # Order: 0.1*x^3 + 0.5*x^2 - 2*x + 5
    coeffs_np = np.array([0.1, 0.5, -2, 5], dtype=float)
    poly = np.poly1d(coeffs_np)

    # Test for some negative and positive x
    for x in range(-2, 3):
        y = poly(x)
        # No assertion needed, just print as in the original (here omitted)

    xx = np.array([-2, -1, 0, 1], dtype=float)
    out = poly(xx)

    # Now use different values for fitting (cubic)
    fit_coeffs = np.polyfit(xx, out, 3)
    polyfit = np.poly1d(fit_coeffs)

    # Check coefficients similarity (should match original, allow some numerical error)
    # Note: polyfit returns highest degree first
    for i, (actual, estimated) in enumerate(zip(coeffs_np, fit_coeffs)):
        assert abs(actual - estimated) < 1e-8, f"public polyfit coeff mismatch at i={i}: got {estimated} expected {actual}"

@pytest.mark.public
def test_public_poly_fit():
    public_fit_test()
    public_test_poly()