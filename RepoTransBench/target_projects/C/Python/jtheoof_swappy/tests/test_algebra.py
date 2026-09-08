import math
import pytest
from src.swappy.algebra import gaussian_kernel, gaussian_kernel_free

def test_gaussian_kernel_basic():
    width = 3
    sigma = 1.0
    kernel = gaussian_kernel(width, sigma)

    assert kernel is not None
    assert kernel.kernel is not None
    assert kernel.size == width * width + 1
    assert kernel.sum > 0
    assert abs(kernel.sigma - sigma) < 1e-6

    gaussian_kernel_free(kernel)

def test_gaussian_kernel_free_null():
    gaussian_kernel_free(None)
    # If we get here without error, the test passes
    assert True