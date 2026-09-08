import numpy as np
import pytest

from src.enigmahuang_poisson_fdm_multigrid.poisson3d_7pt_genmat import Poisson3D_7pt_GenMat
from src.enigmahuang_poisson_fdm_multigrid.multigrid_solver import Multigrid_Solver

def test_poisson3d_smoke():
    for p in [2, 3]:
        n = 2**p - 1
        N = n * n * n
        np.random.seed(n)
        print(f'Using {n} * {n} * {n} initial cube')
        A = Poisson3D_7pt_GenMat(p)
        b = np.random.rand(N) - 0.5
        x, vc_cnt = Multigrid_Solver(A, b, dim=3)
        assert len(x) == N