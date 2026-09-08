import numpy as np
import pytest
from src.spread import spread

def test_basic_expand():
    data = [3, 5]
    code = [0, 2]
    out = spread(data, code)
    expected = np.array([[0, 6, 0, 10]])
    assert np.array_equal(out, expected)

def test_multiple_rows():
    data = np.array([[2, 4], [6, 8]])
    code = np.array([[0, 1], [1, 0]])
    out = spread(data, code)
    assert out.shape == (2, 4)

def test_missing_arg():
    with pytest.raises(TypeError):
        spread([10, 20], None)

def test_code_too_short():
    data = np.array([[2,3], [4,5]])
    code = np.array([0,0])
    with pytest.raises(ValueError):
        spread(data, code)

def test_nonmatching_size():
    data = [2,4]
    code = [8,7,6]
    out = spread(data, code)
    assert out.shape == (1, 6)

def test_zeros_input():
    data = np.zeros(4)
    code = [7,5]
    out = spread(data, code)
    assert np.all(out == 0)
    assert out.shape == (1,8)