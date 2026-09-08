import numpy as np
import pytest

from src.enigmahuang_poisson_fdm_multigrid.poisson1d_3pt_genmat import Poisson1D_3pt_GenMat
from src.enigmahuang_poisson_fdm_multigrid.multigrid1d_vcycle_genmat import Multigrid1D_Vcycle_GenMat

def test_multigrid1d_basic():
    A_initial = Poisson1D_3pt_GenMat(4)
    direct_n = 4
    A_list, R_list, max_level = Multigrid1D_Vcycle_GenMat(A_initial, direct_n)

    assert isinstance(A_list, list)
    assert isinstance(R_list, list)
    assert max_level > 1

    assert A_list[0].shape == A_initial.shape
    assert R_list[0].shape == (np.floor((15-1)/2).astype(int), 15)
    assert R_list[1].shape == (np.floor((7-1)/2).astype(int), 7)
    assert R_list[2].shape == (np.floor((3-1)/2).astype(int), 3)
    assert A_list[max_level-1].shape == (1, 1)

def test_multigrid1d_direct_n_larger_than_a():
    A_initial = Poisson1D_3pt_GenMat(2)
    direct_n = 5
    A_list, R_list, max_level = Multigrid1D_Vcycle_GenMat(A_initial, direct_n)

    assert max_level == 1
    assert len(A_list) == 1
    assert len(R_list) == 0
    assert np.allclose(A_list[0], A_initial)

def test_multigrid1d_direct_n_equal_to_a_n():
    A_initial = Poisson1D_3pt_GenMat(2)
    direct_n = 3
    A_list, R_list, max_level = Multigrid1D_Vcycle_GenMat(A_initial, direct_n)

    assert max_level == 1
    assert len(A_list) == 1
    assert len(R_list) == 0
    assert np.allclose(A_list[0], A_initial)

def test_multigrid1d_min_size():
    A_initial = Poisson1D_3pt_GenMat(1)
    direct_n = 1
    A_list, R_list, max_level = Multigrid1D_Vcycle_GenMat(A_initial, direct_n)
    assert max_level == 1
    assert len(A_list) == 1
    assert len(R_list) == 0
    assert np.allclose(A_list[0], A_initial)