import numpy as np
import pytest

from src.enigmahuang_poisson_fdm_multigrid.poisson3d_7pt_genmat import Poisson3D_7pt_GenMat
from src.enigmahuang_poisson_fdm_multigrid.multigrid_solver import Multigrid_Solver

def test_poisson3d_public_smoke():
    for q in [2, 3]:
        n = 2**q - 1
        N = n*n*n
        np.random.seed(n + 33)
        print(f'PublicTest: Using {n} * {n} * {n} cubic grid')
        A = Poisson3D_7pt_GenMat(q)
        b = np.random.rand(N) - 0.3
        x, vc_cnt = Multigrid_Solver(A, b, dim=3)
        assert len(x) == N