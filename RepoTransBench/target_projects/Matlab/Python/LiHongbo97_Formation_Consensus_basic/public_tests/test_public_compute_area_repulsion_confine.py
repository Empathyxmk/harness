import numpy as np
from lihongbo_consensus.helpers import compute_area, compute_repulsion, confine

def test_public_compute_area_repulsion_confine():
    pnts = np.array([[1, 2], [3, 5], [5, 4], [4, 0]])
    area_v = compute_area(pnts)
    assert area_v > 0

    # Repulsion calculation public edge case
    obj_p = np.array([7, 6])
    obs_p = np.array([[8, 9]])
    rep = compute_repulsion(obj_p, obs_p, 1.5)
    assert isinstance(rep, np.ndarray) and rep.size == 2

    # Confine with different boundaries
    pos = np.array([2, 2])
    lims = np.array([[0, 4], [0, 4]])
    posc = confine(pos, lims)
    assert np.all(posc >= lims[:, 0]) and np.all(posc <= lims[:, 1])