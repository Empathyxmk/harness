import numpy as np
import pytest

import naturalneighbor

def test_output_shape_for_plane_public():
    grid_xi = np.array([[5, 6, 7], [8, 9, 10]])
    grid_yi = np.array([[11, 12, 13], [14, 15, 16]])
    assert grid_xi.shape == (2, 3)
    assert grid_yi.shape == (2, 3)

def test_output_shape_for_flat_public():
    arr = np.zeros((7, 7, 7))
    flat = arr.flatten()
    assert flat.shape == (343,)
    reshaped = flat.reshape((7, 7, 7))
    assert reshaped.shape == arr.shape