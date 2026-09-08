import numpy as np
from tests.original.munkres_helper import munkres

def test_public_munkres():
    costMat_pub = np.array([[6,4,9],[7,2,5],[8,7,6]])
    assignment_pub, cost_pub = munkres(costMat_pub)
    assert isinstance(assignment_pub, np.ndarray)
    assert isinstance(cost_pub, (int, float, np.integer, np.floating))
    assert len(assignment_pub) == costMat_pub.shape[0]