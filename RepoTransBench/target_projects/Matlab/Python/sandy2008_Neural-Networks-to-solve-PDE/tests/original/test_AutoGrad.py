import numpy as np
from src.pde_utils.autograd_full import AutoGrad

def funObj_test(x):
    return float(x[0])**2 + float(x[1])**2 + float(x[0])*float(x[1]) + 5

def test_AutoGrad_type1_forward():
    x_input = np.array([1.0, 2.0])
    f1_actual, g1_actual = AutoGrad(x_input, 1, funObj_test)
    assert abs(f1_actual - 12) < 1e-6
    np.testing.assert_allclose(g1_actual, np.array([4.0, 5.0]), atol=1e-6)

def test_AutoGrad_type3_complex():
    x_input = np.array([1.0, 2.0])
    f3_actual, g3_actual = AutoGrad(x_input, 3, funObj_test)
    assert abs(f3_actual - 12) < 1e-9
    np.testing.assert_allclose(g3_actual, np.array([4.0, 5.0]), atol=1e-9)

def test_AutoGrad_type2_central():
    x_input = np.array([1.0, 2.0])
    f2_actual, g2_actual = AutoGrad(x_input, 2, funObj_test)
    assert abs(f2_actual - 12) < 1e-6
    np.testing.assert_allclose(g2_actual, np.array([4.0, 5.0]), atol=1e-6)

def test_AutoGrad_type1_forward_neg():
    x_input = np.array([-1.0, -2.0])
    f1_neg_actual, g1_neg_actual = AutoGrad(x_input, 1, funObj_test)
    assert abs(f1_neg_actual - 12) < 1e-6
    np.testing.assert_allclose(g1_neg_actual, np.array([-4.0, -5.0]), atol=1e-6)

def test_AutoGrad_type3_complex_neg():
    x_input = np.array([-1.0, -2.0])
    f3_neg_actual, g3_neg_actual = AutoGrad(x_input, 3, funObj_test)
    assert abs(f3_neg_actual - 12) < 1e-9
    np.testing.assert_allclose(g3_neg_actual, np.array([-4.0, -5.0]), atol=1e-9)

def test_AutoGrad_type2_central_neg():
    x_input = np.array([-1.0, -2.0])
    f2_neg_actual, g2_neg_actual = AutoGrad(x_input, 2, funObj_test)
    assert abs(f2_neg_actual - 12) < 1e-6
    np.testing.assert_allclose(g2_neg_actual, np.array([-4.0, -5.0]), atol=1e-6)