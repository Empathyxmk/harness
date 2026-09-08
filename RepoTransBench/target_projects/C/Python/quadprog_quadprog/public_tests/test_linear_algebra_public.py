import numpy as np
import pytest

# Python implementations of the C linear algebra functions for public tests.

def dot(x, y, n):
    """Mimics C's dot product function."""
    return np.dot(x[:n], y[:n])

def add(a, b, c, n):
    """Mimics C's add function (element-wise addition into c)."""
    for i in range(n):
        c[i] = a[i] + b[i]

def norm(v, n):
    """Mimics C's Euclidean norm function."""
    return np.linalg.norm(v[:n])

def test_dot_product_public():
    x = np.array([2.0, -4.5, 1.2])
    y = np.array([-1.0, 3.0, 2.0])
    expected = (2.0 * -1.0 + -4.5 * 3.0 + 1.2 * 2.0)
    result = dot(x, y, 3)
    np.testing.assert_allclose(result, expected, atol=1e-9)

def test_vector_add_public():
    a = np.array([1.0, 2.0])
    b = np.array([3.0, -1.0])
    c = np.zeros(2)
    add(a, b, c, 2)
    np.testing.assert_allclose(c, [4.0, 1.0], atol=1e-9)

def test_vector_norm_public():
    v = np.array([3.0, 4.0, 12.0]) # sqrt(9+16+144) = sqrt(169) = 13
    result = norm(v, 3)
    np.testing.assert_allclose(result, 13.0, atol=1e-9)