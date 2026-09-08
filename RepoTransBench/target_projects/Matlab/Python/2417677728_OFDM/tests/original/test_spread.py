import numpy as np
import pytest
from src.spread import spread

def test_basic_expand():
    data = [1, 2]
    code = [1, 0]
    out = spread(data, code)
    expected = np.array([[1, 0, 2, 0]])
    assert np.array_equal(out, expected)

def test_multiple_rows():
    data = np.array([[1, 2], [3, 4]])
    code = np.array([[1, 1], [0, 1]])
    out = spread(data, code)
    assert out.shape == (2, 4)

def test_missing_arg():
    with pytest.raises(TypeError):
        spread([1, 2], None)

def test_code_too_short():
    data = np.array([[1,2], [3,4]])
    code = np.array([1,1])
    with pytest.raises(ValueError):
        spread(data, code)

def test_nonmatching_size():
    data = [1,2]
    code = [1,2,3]
    out = spread(data, code)
    assert out.shape == (1, 6)

def test_zeros_input():
    data = np.zeros(3)
    code = [1,1]
    out = spread(data, code)
    assert np.all(out == 0)
    assert out.shape == (1,6)