import numpy as np
import pytest

from src.enigmahuang_poisson_fdm_multigrid.multigrid1d_vcycle_genmat import Multigrid1D_Vcycle_GenMat

def test_multigrid1d_vcycle_small_public():
    n = 7
    A = np.diag(np.ones(n)*3) + np.diag(np.ones(n-1)*-1.5,1) + np.diag(np.ones(n-1)*-1.5,-1)
    direct_n = 2
    A_list, R_list, max_level = Multigrid1D_Vcycle_GenMat(A, direct_n)
    assert isinstance(A_list, list)
    assert isinstance(R_list, list)
    assert max_level > 1
    assert max_level <= np.log2(n+1)

def test_multigrid1d_vcycle_medium_public():
    n = 31
    A = np.diag(np.ones(n)*7) + np.diag(np.ones(n-1)*-3,1) + np.diag(np.ones(n-1)*-3,-1)
    direct_n = 5
    A_list, R_list, max_level = Multigrid1D_Vcycle_GenMat(A, direct_n)
    assert len(A_list) == max_level
    assert len(R_list) == max_level - 1
    assert hasattr(R_list[0], 'tocsc') or hasattr(R_list[0], 'tocsr') or (np.count_nonzero(R_list[0]) < np.prod(R_list[0].shape)//8) # is sparse