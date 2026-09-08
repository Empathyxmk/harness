import numpy as np
import pytest

from src.enigmahuang_poisson_fdm_multigrid.poisson2d_5pt_genmat import Poisson2D_5pt_GenMat
from src.enigmahuang_poisson_fdm_multigrid.multigrid_solver import Multigrid_Solver

def test_poisson2d_smoke():
    # Equivalent to test_Poisson2D(p) for several p
    for p in [2, 3]:
        n = 2**p - 1
        N = n * n
        np.random.seed(n)
        print(f'Using {n} * {n} square initial grid')
        A = Poisson2D_5pt_GenMat(p)
        b = np.random.rand(N) - 0.5
        x, vc_cnt = Multigrid_Solver(A, b, dim=2)
        assert len(x) == N