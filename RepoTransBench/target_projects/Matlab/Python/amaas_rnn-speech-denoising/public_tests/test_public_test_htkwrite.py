import os
import numpy as np
from src.htkwrite import htkwrite
from src.htkread import htkread

def test_public_htkwrite_different_data():
    fname = 'tempfile_public_htkwrite.bin'
    data = np.array([[-0.4, 0.9], [1.2, -1.5]], dtype=float)
    try:
        htkwrite(fname, data, 160000, 6)
        data2, h = htkread(fname)
        assert data2.shape == data.shape
        assert abs(data2[1,1] + 1.5) < 1e-6
    finally:
        if os.path.exists(fname):
            os.remove(fname)