import numpy as np
import pytest

from src.enigmahuang_poisson_fdm_multigrid.multigrid3d_vcycle_genmat import Multigrid3D_Vcycle_GenMat

def test_multigrid3d_vcycle_genmat_public():
    n = 7
    A = np.diag(np.ones(n**3)*6)
    direct_n = 3
    A_list, R_list, max_level = Multigrid3D_Vcycle_GenMat(A, direct_n, n)
    assert isinstance(A_list, list)
    assert isinstance(R_list, list)
    assert max_level > 1