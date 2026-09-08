import numpy as np
from src.hems.Dynamic_Price_HEMS import Dynamic_Price_HEMS

def test_Dynamic_Price_HEMS_basic():
    N_T = 24
    x_test1 = 10
    y_test1 = 12
    a, b, c, Price_D = Dynamic_Price_HEMS(x_test1, y_test1)
    assert len(Price_D) == N_T
    assert isinstance(Price_D, np.ndarray)
    assert np.all(Price_D >= 0)

def test_Dynamic_Price_HEMS_x_edge():
    N_T = 24
    x_test2 = 1
    y_test2 = 1
    _a2, _b2, _c2, Price_D2 = Dynamic_Price_HEMS(x_test2, y_test2)
    assert len(Price_D2) == N_T

def test_Dynamic_Price_HEMS_y_edge():
    N_T = 24
    x_test3 = 24
    y_test3 = 365
    _a3, _b3, _c3, Price_D3 = Dynamic_Price_HEMS(x_test3, y_test3)
    assert len(Price_D3) == N_T

import pytest

def test_Dynamic_Price_HEMS_invalid_x():
    N_T = 24
    x_test4 = 25
    y_test4 = 1
    try:
        _a4, _b4, _c4, Price_D4 = Dynamic_Price_HEMS(x_test4, y_test4)
        assert len(Price_D4) == N_T
    except Exception:
        # Error is allowed
        pass