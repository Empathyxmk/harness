import pytest
from src.sp import bpsk_diff
import numpy as np

def test_simple():
    data = np.array([1, 0, 1, 1, 0])
    d = bpsk_diff(data)
    assert len(d) == 5