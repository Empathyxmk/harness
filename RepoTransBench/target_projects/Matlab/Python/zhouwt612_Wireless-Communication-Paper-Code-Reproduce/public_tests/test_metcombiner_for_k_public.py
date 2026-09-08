import numpy as np
import pytest

from src.combining.met import METcombiner_forK

class TestMETcombinerForKPublic:
    def test_different_sizes(self):
        # Use a non-square, non-trivial H
        H = np.zeros((3, 4, 2))
        H[:, :, 0] = np.array([
            [1, 0, 0, 0],
            [0, 2, 0, 0],
            [0, 0, 3, 0]
        ])
        H[:, :, 1] = np.array([
            [4, 1, 0, 0],
            [0, 5, 1, 0],
            [0, 0, 6, 2]
        ])
        L = 2
        H_MET, G_MET = METcombiner_forK(H, L)
        # Size checks
        assert H_MET.shape == (3, 4, 2)
        assert G_MET.shape == (4, 4, 2)
        # Norm checks
        assert np.linalg.norm(H_MET[:, :, 0]) > 0
        assert np.linalg.norm(G_MET[:, :, 1]) > 0

    def test_random_h(self):
        np.random.seed(123)
        H = np.random.randn(4, 2, 3)
        L = 1
        H_MET, G_MET = METcombiner_forK(H, L)
        assert H_MET.shape == (4, 2, 3)
        assert G_MET.shape == (2, 2, 3)
        assert np.linalg.norm(H_MET) > 0
        assert np.linalg.norm(G_MET) > 0