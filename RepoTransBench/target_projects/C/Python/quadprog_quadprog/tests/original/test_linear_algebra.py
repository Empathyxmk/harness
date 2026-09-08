import numpy as np
import pytest

# Python implementations of the C linear algebra functions for testing purposes.
# These mimic the behavior of the C functions tested in test_linear_algebra.c,
# particularly for the specific test cases.

def vector_dot(a, b, n):
    """Mimics C's vector_dot."""
    return np.dot(a[:n], b[:n])

def vector_scale(x, n, factor):
    """Mimics C's vector_scale (in-place)."""
    for i in range(n):
        x[i] *= factor

def vector_add(a, b, out, n):
    """Mimics C's vector_add (stores result in out)."""
    for i in range(n):
        out[i] = a[i] + b[i]

def matrix_vector_mult(A, m, n, x, y):
    """Mimics C's matrix_vector_mult for row-major A, y = A @ x."""
    A_np = np.array(A).reshape((m, n))
    x_np = np.array(x)
    y_np = A_np @ x_np
    for i in range(m):
        y[i] = y_np[i]

def triangular_solve(n, A, b, is_lower, x):
    """Mimics C's triangular_solve.
    A is assumed to be a flattened matrix (n*n elements).
    is_lower=1 for lower triangular, 0 for upper.
    """
    A_np = np.array(A).reshape((n, n))
    b_np = np.array(b)
    
    if is_lower:
        # Lower triangular solve
        x_np = np.linalg.solve(A_np, b_np)
    else:
        # Upper triangular solve
        x_np = np.linalg.solve(A_np, b_np)
    
    for i in range(n):
        x[i] = x_np[i]

def test_vector_dot_fn():
    a = np.array([1.0, 2.0, 3.0])
    b = np.array([4.0, 5.0, 6.0])
    expected = 1.0*4.0 + 2.0*5.0 + 3.0*6.0
    result = vector_dot(a, b, 3)
    np.testing.assert_allclose(result, expected, atol=1e-9)

def test_vector_scale_fn():
    x = np.array([2.0, -2.0, 0.5])
    expected = np.array([4.0, -4.0, 1.0])
    vector_scale(x, 3, 2.0)
    np.testing.assert_allclose(x, expected, atol=1e-9)

def test_vector_add_fn():
    a = np.array([1.0, 1.0, 1.0])
    b = np.array([2.0, 3.0, 4.0])
    out = np.zeros(3)
    expected = np.array([3.0, 4.0, 5.0])
    vector_add(a, b, out, 3)
    np.testing.assert_allclose(out, expected, atol=1e-9)

def test_matrix_vector_mult_fn():
    A = np.array([1,2,3,4,5,6]) # 2x3 (row-major)
    x = np.array([1,2,3])
    y = np.zeros(2)
    expected = np.array([1*1+2*2+3*3, 4*1+5*2+6*3])
    matrix_vector_mult(A, 2, 3, x, y)
    np.testing.assert_allclose(y, expected, atol=1e-9)

def test_triangular_solve_fn():
    # lower-triangular: solve n=2, a = [1 0; 2 1], b = [5,7]
    L = np.array([1,0,2,1])
    b = np.array([5, 7])
    expected = np.array([5, -3])
    x = np.zeros(2)
    triangular_solve(2, L, b, 1, x) # lower
    np.testing.assert_allclose(x, expected, atol=1e-9)

    # upper-triangular: [2,3;0,1] solve x, b=[7,1]
    U = np.array([2,3,0,1])
    bu = np.array([7, 1])
    exc = np.array([2,1])
    xu = np.zeros(2)
    triangular_solve(2, U, bu, 0, xu) # upper
    np.testing.assert_allclose(xu, exc, atol=1e-9)