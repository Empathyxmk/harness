import numpy as np
import pytest

from src.enigmahuang_poisson_fdm_multigrid.poisson1d_3pt_genmat import Poisson1D_3pt_GenMat
from src.enigmahuang_poisson_fdm_multigrid.poisson2d_5pt_genmat import Poisson2D_5pt_GenMat
from src.enigmahuang_poisson_fdm_multigrid.poisson3d_7pt_genmat import Poisson3D_7pt_GenMat
from src.enigmahuang_poisson_fdm_multigrid.multigrid_solver import Multigrid_Solver
from src.enigmahuang_poisson_fdm_multigrid.gs_iter import GS_Iter
from src.enigmahuang_poisson_fdm_multigrid.jacobi_iter import Jacobi_Iter

def assert_vectors_almost_equal(x, y, tol=1e-4):
    np.testing.assert_allclose(x, y, atol=tol)

def create_simple_poisson_matrix(dim, p):
    if dim == 1:
        return Poisson1D_3pt_GenMat(p)
    elif dim == 2:
        return Poisson2D_5pt_GenMat(p)
    elif dim == 3:
        return Poisson3D_7pt_GenMat(p)
    else:
        raise ValueError('Invalid dimension')

def test_multigrid_solver_1d_basic():
    p = 4
    A = create_simple_poisson_matrix(1, p)
    n = A.shape[0]
    x_exact = np.sin(np.linspace(0, np.pi, n+2))[1:-1]
    b = A @ x_exact
    x_solved, vcycle_cnt, res_norm = Multigrid_Solver(A, b, dim=1)
    assert_vectors_almost_equal(x_solved, x_exact, tol=1e-4)
    assert vcycle_cnt > 0
    assert res_norm[-1] < 1e-9

def test_multigrid_solver_1d_custom_smoother_jacobi():
    p = 4
    A = create_simple_poisson_matrix(1, p)
    n = A.shape[0]
    x_exact = np.sin(np.linspace(0, np.pi, n+2))[1:-1]
    b = A @ x_exact
    x_solved, vcycle_cnt, res_norm = Multigrid_Solver(A, b, dim=1, smoother=Jacobi_Iter, pre_steps=2, post_steps=2, tol=1e-8)
    assert_vectors_almost_equal(x_solved, x_exact, tol=1e-3)
    assert vcycle_cnt > 0
    assert res_norm[-1] < 1e-7

def test_multigrid_solver_1d_max_iter_pre_pos_steps():
    p = 3
    A = create_simple_poisson_matrix(1, p)
    n = A.shape[0]
    x_exact = np.arange(1, n+1)
    b = A @ x_exact
    x_solved, vcycle_cnt, res_norm = Multigrid_Solver(A, b, dim=1, smoother=GS_Iter, pre_steps=3, post_steps=3, tol=1e-9)
    assert_vectors_almost_equal(x_solved, x_exact, tol=1e-5)
    assert vcycle_cnt > 0
    assert res_norm[-1] < 1e-8

def test_multigrid_solver_2d_basic():
    p = 3
    A = create_simple_poisson_matrix(2, p)
    N = A.shape[0]
    x_exact = np.random.rand(N)
    b = A @ x_exact
    x_solved, vcycle_cnt, res_norm = Multigrid_Solver(A, b, dim=2)
    assert_vectors_almost_equal(x_solved, x_exact, tol=1e-3)
    assert vcycle_cnt > 0
    assert res_norm[-1] < 1e-9

def test_multigrid_solver_3d_basic():
    p = 2
    A = create_simple_poisson_matrix(3, p)
    N = A.shape[0]
    x_exact = np.random.rand(N)
    b = A @ x_exact
    x_solved, vcycle_cnt, res_norm = Multigrid_Solver(A, b, dim=3)
    assert_vectors_almost_equal(x_solved, x_exact, tol=1e-2)
    assert vcycle_cnt > 0
    assert res_norm[-1] < 1e-9

def test_multigrid_solver_convergence_tolerance():
    p = 4
    A = create_simple_poisson_matrix(1, p)
    n = A.shape[0]
    x_exact = np.ones(n)
    b = A @ x_exact
    tol = 1e-6
    x_solved, vcycle_cnt, res_norm = Multigrid_Solver(A, b, dim=1, smoother=GS_Iter, pre_steps=1, post_steps=1, tol=tol)
    assert_vectors_almost_equal(x_solved, x_exact, tol=1e-5)
    assert res_norm[-1] < np.linalg.norm(b) * tol * 1.1

def test_multigrid_solver_non_converging_case():
    p = 2
    A = create_simple_poisson_matrix(1, p)
    n = A.shape[0]
    b = np.random.rand(n)
    x_solved, vcycle_cnt, res_norm = Multigrid_Solver(A, b, dim=1, smoother=GS_Iter, pre_steps=1, post_steps=1, tol=0.5)
    assert vcycle_cnt > 0
    assert res_norm[-1] < np.linalg.norm(b)*0.5 + np.finfo(float).eps