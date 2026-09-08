import numpy as np
from ukfmanifold.quaternions import isq

def test_public_isq_various():
    assert isq(np.array([1,2,3,4])) == 1
    assert isq(np.ones((1,4))) == 2
    assert isq(np.ones((4,1))) == 1