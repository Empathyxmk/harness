import pytest
import numpy as np

from src.lips.bryant2angular import bryant2angular

def test_zero_input():
    ang = bryant2angular([0, 0, 0])
    np.testing.assert_array_equal(ang, [0, 0, 0])

def test_standard_input():
    v = [np.pi/2, np.pi/4, -np.pi/6]
    ang = bryant2angular(v)
    assert np.asarray(ang).shape == (3,)

def test_vector_input():
    v = [0.1, 0.2, 0.3]
    ang = bryant2angular(v)
    assert isinstance(ang, (list, np.ndarray))

def test_error_on_wrong_input():
    with pytest.raises(Exception):
        bryant2angular([1, 2])