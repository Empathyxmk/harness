import numpy as np
import pytest

from src.unmix.prune_library import prune_library

def test_empty_input():
    A = np.empty((0,0))
    min_angle = 10
    B = prune_library(A, min_angle)
    assert B.shape == (0, 0)
    assert B.size == 0

def test_single_column():
    A = np.array([[1], [2], [3]])
    min_angle = 10
    B = prune_library(A, min_angle)
    assert np.allclose(B, A, atol=1e-9)

def test_no_pruning_needed():
    A = np.array([[1,0],[0,1]])
    min_angle = 45
    B = prune_library(A, min_angle)
    assert np.allclose(B, A, atol=1e-9)

def test_pruning_similar_columns():
    A = np.array([[1, 1.01, 0], [0, 0.01, 1]])
    min_angle = 5
    expectedB = np.array([[1,0],[0,1]])
    actualB = prune_library(A, min_angle)
    assert actualB.shape == expectedB.shape
    # sort columns for comparison
    assert np.isclose(np.linalg.norm(np.sort(actualB,axis=1)-np.sort(expectedB,axis=1)), 0, atol=1e-9)

def test_all_columns_similar():
    A = np.array([[1, 1.01, 1.005], [2, 2.02, 2.01]])
    min_angle = 1
    expectedB = A[:,[0]]
    actualB = prune_library(A, min_angle)
    assert np.allclose(actualB, expectedB, atol=1e-9)

def test_edge_case_min_angle_zero():
    A = np.array([[1, 1.01, 0], [0, 0.01, 1]])
    min_angle = 0
    B = prune_library(A, min_angle)
    assert np.allclose(B, A, atol=1e-9)

def test_edge_case_min_angle_180():
    A = np.array([[1, -1, 0], [0, 0, 1]])
    min_angle = 180
    expectedB = A[:,[0]]
    actualB = prune_library(A, min_angle)
    assert np.allclose(actualB, expectedB, atol=1e-9)

def test_columns_with_zeros():
    A = np.identity(3)
    min_angle = 45
    B = prune_library(A, min_angle)
    assert np.allclose(B, A, atol=1e-9)

def test_duplicate_columns():
    A = np.array([[1,1,0],[0,0,1]])
    min_angle = 5
    expectedB = np.array([[1,0],[0,1]])
    actualB = prune_library(A, min_angle)
    assert actualB.shape == expectedB.shape
    assert np.allclose(np.sort(actualB,axis=1), np.sort(expectedB,axis=1), atol=1e-9)