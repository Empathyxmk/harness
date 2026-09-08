import pytest
import numpy as np
from src.differential_evolution import differentail_evolution

class TestDifferentialEvolution:
    def test_default_run(self):
        BestS, Best_f_final, time_log, Best_f_log = differentail_evolution()
        # Shape assertions
        assert BestS.shape == (2,), "BestS shape"
        assert -2.048 <= BestS[0] <= 2.048
        assert -2.048 <= BestS[1] <= 2.048
        assert isinstance(Best_f_final, float) or isinstance(Best_f_final, np.floating)
        assert np.isscalar(Best_f_final)
        assert Best_f_final >= 0
        assert time_log.shape == (1, 50)
        assert Best_f_log.shape == (1, 50)

    def test_specific_parameters(self):
        Size, CodeL = 10, 2
        MinX, MaxX = [-1, -1], [1, 1]
        G = 10
        F, cr = 0.5, 0.8
        BestS, Best_f, time_log, Best_f_log = differentail_evolution(Size, CodeL, MinX, MaxX, G, F, cr)
        assert BestS.shape == (2,), "BestS shape specific"
        assert MinX[0] <= BestS[0] <= MaxX[0]
        assert MinX[1] <= BestS[1] <= MaxX[1]
        assert isinstance(Best_f, float) or isinstance(Best_f, np.floating)
        assert Best_f >= 0
        assert time_log.shape == (1, G)
        assert Best_f_log.shape == (1, G)

    def test_edge_case_parameters(self):
        # Minimum viable size so that r1, r2, r3 are all non-i and unique
        Size, CodeL = 4, 1
        MinX, MaxX = [0], [1]
        G = 1
        F, cr = 0.1, 0.1
        BestS, Best_f, _, _ = differentail_evolution(Size, CodeL, MinX, MaxX, G, F, cr)
        assert BestS.shape == (1,)
        assert MinX[0] <= BestS[0] <= MaxX[0]
        assert Best_f >= 0

    def test_bounds_clamping(self):
        Size, CodeL = 5, 2
        G = 1
        F, cr = 2.0, 0.5
        MinX, MaxX = [0, 0], [1, 1]
        BestS, _, _, _ = differentail_evolution(Size, CodeL, MinX, MaxX, G, F, cr)
        assert MinX[0] <= BestS[0] <= MaxX[0]
        assert MinX[1] <= BestS[1] <= MaxX[1]