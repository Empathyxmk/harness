import pytest
from src.sp import find_nearest_pos
import numpy as np

def test_near_left():
    pos = find_nearest_pos(np.array([2,7,8,4]), 5)
    assert pos == 0 or pos == 3

def test_near_right():
    pos = find_nearest_pos(np.array([-3,0,9,6]), 8)
    assert pos == 2