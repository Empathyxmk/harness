import os
import numpy as np
from src.htkread import htkread, htkwrite

def test_htkread_simple_artificial_file():
    fname = "tmp_htkfile_htkread.bin"
    try:
        with open(fname, "wb") as f:
            f.write((2).to_bytes(4, byteorder='big', signed=True))      # Nsamples
            f.write((100000).to_bytes(4, byteorder='big', signed=True)) # Sample period
            f.write((4).to_bytes(2, byteorder='big', signed=True))      # Sample size (bytes)
            f.write((9).to_bytes(2, byteorder='big', signed=True))      # Param kind
            arr = np.array([[0.5, 0.7], [-0.3, 0.8]], dtype='>f4')
            arr.tofile(f)
        data, h = htkread(fname)
        assert data.shape == (2, 2)
        assert h['Nsamples'] == 2
    finally:
        if os.path.exists(fname):
            os.remove(fname)