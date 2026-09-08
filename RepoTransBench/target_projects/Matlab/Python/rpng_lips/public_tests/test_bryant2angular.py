import pytest
import numpy as np

from src.lips.bryant2angular import bryant2angular

def test_simple_case():
    b = np.pi / 6
    r = np.pi / 3
    y = np.pi / 2
    output = bryant2angular([b, r, y])
    out_expected = [np.pi / 2, np.pi / 6, np.pi / 3]
    np.testing.assert_allclose(output, out_expected, atol=1e-10)

def test_negative_angles():
    b = -np.pi / 5
    r = -np.pi / 7
    y = -np.pi / 8
    output = bryant2angular([b, r, y])
    out_expected = [-np.pi / 8, -np.pi / 5, -np.pi / 7]
    np.testing.assert_allclose(output, out_expected, atol=1e-10)