import numpy as np
import pytest

from src.enigmahuang_poisson_fdm_multigrid.poisson1d_3pt_genmat import Poisson1D_3pt_GenMat
from src.enigmahuang_poisson_fdm_multigrid.multigrid_solver import Multigrid_Solver

def test_poisson1d_smoke():
    for p in [2, 3]:
        n = 2**p - 1
        np.random.seed(n)
        print(f'Using {n} initial grid points')
        A = Poisson1D_3pt_GenMat(p)
        b = np.random.rand(n) - 0.5
        x, vc_cnt = Multigrid_Solver(A, b, dim=1)
        assert len(x) == n