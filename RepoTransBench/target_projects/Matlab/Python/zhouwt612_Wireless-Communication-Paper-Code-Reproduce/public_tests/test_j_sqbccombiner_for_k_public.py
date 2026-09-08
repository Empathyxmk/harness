import numpy as np
import pytest

from src.combining.sqbc import J_SQBCcombiner_forK

class TestJ_SQBCcombiner_forKPublic:
    def test_random_matrix_small(self):
        # Use 2x3x2 random input
        np.random.seed(42)
        H = np.random.randn(2, 3, 2)
        L = 1
        G_SQBC, Heff = J_SQBCcombiner_forK(H, L)

        # Check sizes
        assert G_SQBC.shape == (3, 3, 2), "G_SQBC size mismatch"
        assert Heff.shape == (2, 3, 2), "Heff size mismatch"

        # Not all zeros
        assert np.linalg.norm(G_SQBC) > 0
        assert np.linalg.norm(Heff) > 0

    def test_l_greater_than_one(self):
        # Test with L = 2, square matrix K=1
        H = np.array([[1, 2], [-1, 3]], dtype=float)
        H = np.tile(H[:, :, np.newaxis], (1, 1, 1))  # K=1
        L = 2
        G_SQBC, Heff = J_SQBCcombiner_forK(H, L)

        assert G_SQBC.shape == (2, 2, 1)
        assert Heff.shape == (2, 2, 1)
        assert np.linalg.norm(G_SQBC) > 0
        assert np.linalg.norm(Heff) > 0