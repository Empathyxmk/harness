import numpy as np
from ukfmanifold.quaternions import isnormq, qnorm

def test_single_quaternion():
    q = np.array([1,0,0,0])
    assert isnormq(q) == 0

def test_col_stack():
    Q = np.random.randn(4,3)
    Qn = qnorm(Q)
    assert isnormq(Qn) == 1 or isnormq(Qn)==3

def test_row_stack():
    Q = np.random.randn(3,4)
    Qn = qnorm(Q)
    assert isnormq(Qn) == 2 or isnormq(Qn)==3