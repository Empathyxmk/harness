import os
import numpy as np
from src.htkwrite import htkwrite, htkread

def test_htkwrite_write_and_readback():
    fname = 'tempfile_htkwrite.bin'
    data = np.array([[0.2, 0.3], [0.5, 0.7]], dtype=float)
    try:
        htkwrite(fname, data, 80000, 9)
        data2, h = htkread(fname)
        assert data2.shape == data.shape
        assert abs(data2[0,0] - 0.2) < 1e-6
    finally:
        if os.path.exists(fname):
            os.remove(fname)