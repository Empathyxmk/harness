import numpy as np
import pytest

from src.enigmahuang_poisson_fdm_multigrid.poisson1d_3pt_genmat import Poisson1D_3pt_GenMat
from src.enigmahuang_poisson_fdm_multigrid.multigrid_solver import Multigrid_Solver

def test_poisson1d_public_smoke():
    for q in [2, 3]:
        n = 2**q - 1
        np.random.seed(n + 101)
        A = Poisson1D_3pt_GenMat(q)
        b = np.random.rand(n) - 0.4
        x, vc_cnt = Multigrid_Solver(A, b, dim=1)
        assert len(x) == n