import pytest
import numpy as np
from src.differential_evolution import differentail_evolution

class TestDifferentialEvolutionPublic:
    def test_alt_default_run(self):
        BestS, Best_f_final, time_log, Best_f_log = differentail_evolution()
        assert BestS.shape == (2,)
        assert -1.5 <= BestS[0] <= 2.048
        assert -2.048 <= BestS[1] <= 1.5
        assert isinstance(Best_f_final, float) or isinstance(Best_f_final, np.floating)
        assert np.isscalar(Best_f_final)
        assert Best_f_final >= 0
        assert time_log.shape == (1, 50)
        assert Best_f_log.shape == (1, 50)

    def test_other_specific_parameters(self):
        Size, CodeL = 12, 2
        MinX, MaxX = [-0.5, -0.333], [0.5, 0.9]
        G = 8
        F, cr = 0.7, 0.85
        BestS, Best_f, time_log, Best_f_log = differentail_evolution(Size, CodeL, MinX, MaxX, G, F, cr)
        assert BestS.shape == (2,)
        assert MinX[0] <= BestS[0] <= MaxX[0]
        assert MinX[1] <= BestS[1] <= MaxX[1]
        assert isinstance(Best_f, float) or isinstance(Best_f, np.floating)
        assert Best_f >= 0
        assert time_log.shape == (1, G)
        assert Best_f_log.shape == (1, G)

    def test_edge_other_parameters(self):
        Size, CodeL = 5, 1
        MinX, MaxX = [0.1], [2.5]
        G = 2
        F, cr = 0.2, 0.2
        BestS, Best_f, _, _ = differentail_evolution(Size, CodeL, MinX, MaxX, G, F, cr)
        assert BestS.shape == (1,)
        assert MinX[0] <= BestS[0] <= MaxX[0]
        assert Best_f >= 0

    def test_bounds_clamping_public(self):
        Size, CodeL = 6, 2
        G = 2
        F, cr = 3.5, 0.75
        MinX, MaxX = [-10, -4], [-7, -2]
        BestS, _, _, _ = differentail_evolution(Size, CodeL, MinX, MaxX, G, F, cr)
        assert MinX[0] <= BestS[0] <= MaxX[0]
        assert MinX[1] <= BestS[1] <= MaxX[1]