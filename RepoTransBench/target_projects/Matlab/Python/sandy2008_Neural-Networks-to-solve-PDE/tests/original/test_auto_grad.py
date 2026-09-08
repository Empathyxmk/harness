import numpy as np
from src.pde_utils.auto_grad import auto_grad

def funObj_test(x):
    x = np.array(x)
    return x[0]**2 + x[1]**2 + x[0]*x[1] + 5

def test_auto_grad_case1():
    x_input1 = np.array([1.0, 2.0])
    f_actual1, g_actual1 = auto_grad(x_input1, funObj_test)
    assert abs(f_actual1 - 12) < 1e-6
    np.testing.assert_allclose(g_actual1, np.array([4.0, 5.0]), atol=1e-6)

def test_auto_grad_case2():
    x_input2 = np.array([0.0, 0.0])
    f_actual2, g_actual2 = auto_grad(x_input2, funObj_test)
    assert abs(f_actual2 - 5) < 1e-6
    np.testing.assert_allclose(g_actual2, np.array([0.0, 0.0]), atol=1e-6)

def test_auto_grad_case3():
    x_input3 = np.array([-1.0, -2.0])
    f_actual3, g_actual3 = auto_grad(x_input3, funObj_test)
    assert abs(f_actual3 - 12) < 1e-6
    np.testing.assert_allclose(g_actual3, np.array([-4.0, -5.0]), atol=1e-6)