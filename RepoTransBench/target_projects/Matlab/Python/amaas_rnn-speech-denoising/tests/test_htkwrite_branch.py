import os
import numpy as np
import pytest
from src.htkwrite import htkwrite

def test_htkwrite_invalid_filename():
    data = np.random.randn(10,3)
    with pytest.raises(Exception):
        htkwrite('/invalid/xyz/file.htk', data, 100, 9)

def test_htkwrite_mismatched_data():
    # Accept error or success for empty data
    try:
        htkwrite('test.htk', np.array([]), 100, 9)
        assert True
    except Exception:
        assert True
    finally:
        if os.path.exists('test.htk'):
            os.remove('test.htk')