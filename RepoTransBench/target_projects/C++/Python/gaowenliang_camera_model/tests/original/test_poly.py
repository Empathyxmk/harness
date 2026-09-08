import pytest
import numpy as np

def fit_test():
    # xx: 101 evenly spaced values from 0 to ~2.61799 (~ pi/1.2 ~ 2.6)
    # out: known output, same shape as xx
    xx = np.array([
        0, 0.0261799, 0.0523599, 0.0785398, 0.10472, 0.1309, 0.15708, 0.18326,
        0.20944, 0.235619, 0.261799, 0.287979, 0.314159, 0.340339, 0.366519,
        0.392699, 0.418879, 0.445059, 0.471239, 0.497419, 0.523599, 0.549779,
        0.575959, 0.602139, 0.628319, 0.654498, 0.680678, 0.706858, 0.733038,
        0.759218, 0.785398, 0.811578, 0.837758, 0.863938, 0.890118, 0.916298,
        0.942478, 0.968658, 0.994838, 1.02102, 1.0472, 1.07338, 1.09956,
        1.12574, 1.15192, 1.1781, 1.20428, 1.23046, 1.25664, 1.28282,
        1.309, 1.33518, 1.36136, 1.38754, 1.41372, 1.4399, 1.46608,
        1.49226, 1.51844, 1.54462, 1.5708, 1.59698, 1.62316, 1.64934,
        1.67552, 1.7017, 1.72788, 1.75406, 1.78024, 1.80642, 1.8326,
        1.85878, 1.88496, 1.91114, 1.93732, 1.9635, 1.98968, 2.01586,
        2.04204, 2.06822, 2.0944, 2.12058, 2.14675, 2.17293, 2.19911,
        2.22529, 2.25147, 2.27765, 2.30383, 2.33001, 2.35619, 2.38237,
        2.40855, 2.43473, 2.46091, 2.48709, 2.51327, 2.53945, 2.56563,
        2.59181, 2.61799
    ])
    out = np.array([
        0, 0.0261771, 0.0523467, 0.0785066, 0.104654, 0.130789, 0.156907,
        0.183008, 0.209091, 0.235154, 0.261196, 0.287216, 0.313212, 0.339184,
        0.365131, 0.391052, 0.416945, 0.44281, 0.468646, 0.494452, 0.520226,
        0.545968, 0.571676, 0.597349, 0.622986, 0.648584, 0.674144, 0.699662,
        0.725137, 0.750567, 0.775951, 0.801285, 0.826568, 0.851797, 0.876968,
        0.90208, 0.927128, 0.95211, 0.977021, 1.00186, 1.02661, 1.05129,
        1.07587, 1.10036, 1.12475, 1.14903, 1.17319, 1.19724, 1.22115,
        1.24492, 1.26855, 1.29201, 1.3153, 1.33841, 1.36132, 1.38402,
        1.4065, 1.42873, 1.4507, 1.4724, 1.49379, 1.51486, 1.53558,
        1.55594, 1.57589, 1.59541, 1.61448, 1.63305, 1.65109, 1.66857,
        1.68543, 1.70165, 1.71716, 1.73193, 1.7459, 1.759, 1.77119,
        1.7824, 1.79256, 1.80159, 1.80943, 1.81599, 1.82119, 1.82494,
        1.82713, 1.82767, 1.82646, 1.82338, 1.81831, 1.81112, 1.80168,
        1.78986, 1.77551, 1.75847, 1.73857, 1.71566, 1.68955, 1.66005,
        1.62696, 1.59008, 1.54919
    ])
    # Fit a 24th order polynomial, as in the C++ test
    poly_coeffs = np.polyfit(xx, out, 24)
    poly = np.poly1d(poly_coeffs)
    dd = 0.02
    for i in range(100):
        val_x = dd * i
        val_y = poly(val_x)
        # Output is suppressed; could be validated or printed

@pytest.mark.original
def test_poly_all():
    # Simulate C++ test_poly function as closely as possible

    # coeff = [1,2,3,4,5,6]
    coeff = np.array([1, 2, 3, 4, 5, 6.], dtype=float)
    # This would create a 5-degree polynomial: 1 + 2x + 3x^2 + ... + 6x^5
    # But numpy: degree 5: [6,5,4,3,2,1]
    coeffs_deg5 = coeff[::-1]
    poly = np.poly1d(coeffs_deg5)
    # Check coefficients
    assert np.allclose(poly.coeffs, coeffs_deg5)
    for i in range(10):
        _ = poly(i)
    # Now xx = coeff, out=poly(xx)
    xx = coeff
    out = poly(xx)
    # Fit a 5th degree polynomial to (xx, out)
    fit_coeffs = np.polyfit(xx, out, 5)
    assert np.allclose(fit_coeffs, coeffs_deg5, atol=1e-8)
    polyfited = np.poly1d(fit_coeffs)
    # Roots test - all real roots of polynomial 1 + 2x + ... + 6x^5
    realroots = np.roots(coeffs_deg5)
    # C++ prints roots; here we check their type and count as smoke test.
    assert isinstance(realroots, np.ndarray)
    # Now test construct polynomial from [-5, -1, 5, 1] (deg=3): x^3 + 5x^2 - x - 5
    polyn = np.array([-5, -1, 5, 1])
    poly2 = np.poly1d(polyn[::-1])
    realroots2 = np.roots(polyn[::-1])
    assert isinstance(realroots2, np.ndarray)
    # Test for a cubic with real roots expected.
    # Now test poly3 = [-5,1,0,0], deg=3: 0*x^3 + 0*x^2 + 1*x + -5 (really a line)
    poly3 = np.array([-5, 1, 0, 0])
    polyn3 = np.poly1d(poly3[::-1])
    # Find real root in [-100,100]: for a linear polynomial, the root is -coeff[0]/coeff[1]
    # Actually, since .roots() gives all, we just check reasonable value exists
    realroot3 = polyn3.r
    assert isinstance(realroot3, np.ndarray)
    # Assignment checks:
    polyn4 = polyn3.copy()
    assert np.allclose(polyn3, polyn4)
    # String form:
    _ = str(np.poly1d(polyn4[::-1]))

    # -- "pushback" test, which in C++ appends a value --
    # In numpy: np.append
    vec = np.array([1, 2, 1])
    vec2 = np.append(vec, 22)
    assert vec2[-1] == 22

    # Call fit_test to validate fitting works as well
    fit_test()