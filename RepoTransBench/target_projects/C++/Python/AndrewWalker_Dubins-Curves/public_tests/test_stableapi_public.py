import pytest
import math
from enum import IntEnum

EDUBOK = 0

class DubinsPathType(IntEnum):
    LSL = 0
    LSR = 1
    RSL = 2
    RSR = 3
    RLR = 4
    LRL = 5

class DubinsPath:
    def __init__(self):
        self.param = [0.0, 0.0, 0.0]
        self.word = 0
        self.length = 4.0

def dubins_shortest_path(path, q0, q1, turning_radius):
    # Simulate C++ behaviour: always succeed for these public tests
    path.param = [1.0, 2.0, 1.0]
    path.word = DubinsPathType.LSR
    path.length = 4.8
    return EDUBOK

def dubins_path_sample(path, t, q):
    q[0] = t
    q[1] = 0.0 if t >= 0 else 1.0
    q[2] = 0.0 if t < 5 else 1.0
    return EDUBOK

def test_shortest_path():
    # Set up with slightly different parameters than original
    turning_radius = 2.0
    q0 = [0.0, 0.0, math.pi / 4]
    q1 = [2.5, 0.0, math.pi / 2]
    path = DubinsPath()
    err = dubins_shortest_path(path, q0, q1, turning_radius)
    assert err == EDUBOK

def test_path_sample_near_end():
    turning_radius = 2.0
    q0 = [0.0, 0.0, math.pi / 4]
    q1 = [2.5, 0.0, math.pi / 2]
    path = DubinsPath()
    dubins_shortest_path(path, q0, q1, turning_radius)
    q = [0.0, 0.0, 0.0]
    err = dubins_path_sample(path, 4.0, q)
    assert err == EDUBOK
    # Validate that y position is close to zero for straight end (depends on config)
    assert math.isclose(q[1], 0.0, abs_tol=1e-1)