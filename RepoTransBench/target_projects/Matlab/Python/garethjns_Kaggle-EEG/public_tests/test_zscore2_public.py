import pytest
import numpy as np
from src.eeg_kaggle.zscore2 import zscore2

def test_zscore2_different_input():
    data = np.array([[1,3,5],[7,9,11]])
    z = zscore2(data)
    assert z.shape == data.shape
    assert abs(np.mean(z)) < 1e-12