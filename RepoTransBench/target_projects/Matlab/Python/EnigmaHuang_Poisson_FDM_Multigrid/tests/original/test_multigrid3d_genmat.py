import numpy as np
import pytest

from src.enigmahuang_poisson_fdm_multigrid.poisson3d_7pt_genmat import Poisson3D_7pt_GenMat
from src.enigmahuang_poisson_fdm_multigrid.multigrid3d_vcycle_genmat import Multigrid3D_Vcycle_GenMat

def test_multigrid3d_basic():
    A_initial = Poisson3D_7pt_GenMat(2)
    direct_N = 10
    A_list, R_list, max_level = Multigrid3D_Vcycle_GenMat(A_initial, direct_N)

    assert isinstance(A_list, list)
    assert isinstance(R_list, list)
    assert max_level > 1

    assert A_list[0].shape == A_initial.shape
    assert R_list[0].shape == (1, 27)
    assert A_list[1].shape == (1, 1)
    assert max_level == 2

def test_multigrid3d_direct_N_larger_than_a():
    A_initial = Poisson3D_7pt_GenMat(1)
    direct_N = 5
    A_list, R_list, max_level = Multigrid3D_Vcycle_GenMat(A_initial, direct_N)
    assert max_level == 1
    assert len(A_list) == 1
    assert len(R_list) == 0
    assert np.allclose(A_list[0], A_initial)

def test_multigrid3d_direct_N_equal_to_A_N():
    A_initial = Poisson3D_7pt_GenMat(1)
    direct_N = 1
    A_list, R_list, max_level = Multigrid3D_Vcycle_GenMat(A_initial, direct_N)
    assert max_level == 1
    assert len(A_list) == 1
    assert len(R_list) == 0
    assert np.allclose(A_list[0], A_initial)

def test_multigrid3d_larger_system():
    A_initial = Poisson3D_7pt_GenMat(3)
    direct_N = 27
    A_list, R_list, max_level = Multigrid3D_Vcycle_GenMat(A_initial, direct_N)
    assert max_level > 1
    assert A_list[0].shape == (343, 343)
    assert R_list[0].shape == (np.floor((7-1)/2)**3.astype(int), 343)
    assert A_list[1].shape == (27, 27)
    assert R_list[1].shape == (np.floor((3-1)/2)**3.astype(int), 27)
    assert A_list[2].shape == (1, 1)
    assert max_level == 3