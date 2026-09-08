import numpy as np
from lihongbo_consensus.helpers import compute_area, compute_repulsion, confine

def test_compute_area_repulsion_confine():
    P = np.array([[0, 0], [1, 0], [0, 1]])
    area = compute_area(P)
    assert area > 0

    p = np.array([1, 1])
    group = np.array([[0, 0], [2, 2]])
    rep = compute_repulsion(p, group, 1.5, 2, 1)
    assert rep.shape == (2,)

    pos = np.array([2, 3])
    bound = np.array([[0, 5], [0, 5]])
    inside = confine(pos, bound)
    assert np.all(inside == pos)
    outside = confine(np.array([6, 3]), bound)
    assert not np.all(outside == np.array([6, 3]))