import numpy as np
import pytest

from src.unmix.prune_library import prune_library

def test_empty_output():
    # All vectors are colinear, should remove all if min_angle=90
    A = np.array([[1,2],[2,4],[3,6]])
    min_angle = 90
    B = prune_library(A, min_angle)
    assert B.shape[1] == 0 or B.size == 0

def test_one_vector():
    A = np.array([[8],[6],[4]])
    min_angle = 60
    B = prune_library(A, min_angle)
    assert B.shape == (3, 1)
    assert np.allclose(B, A, atol=1e-10)

def test_two_orthogonal():
    A = np.array([[1,0],[0,1],[0,0]])
    min_angle = 85
    B = prune_library(A, min_angle)
    assert B.shape == (3, 2)
    assert np.allclose(B, A, atol=1e-10)

def test_random_small():
    np.random.seed(2)
    A = np.random.rand(3,5)
    min_angle = 2
    B = prune_library(A, min_angle)
    assert B.shape[1] >= 1
    assert B.shape[0] == 3