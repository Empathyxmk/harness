import numpy as np
from py_ir1d_darkface_eval_tools.boxoverlap import boxoverlap

def test_no_overlap():
    boxa = np.array([[10, 10, 20, 20]])
    boxb = np.array([30, 30, 40, 40])
    overlap = boxoverlap(boxa, boxb)
    assert overlap == 0

def test_full_overlap():
    boxa = np.array([[5, 5, 15, 15]])
    boxb = np.array([5, 5, 15, 15])
    overlap = boxoverlap(boxa, boxb)
    assert overlap == 1

def test_partial_overlap():
    boxa = np.array([[0, 0, 20, 20]])
    boxb = np.array([10, 10, 30, 30])
    # Compute expected (Matlab-like): overlapping area 11x11, each box area 21x21
    # But in Matlab test, intersection is 10x10, box size is 20x20, so keep that convention
    expected_overlap = (10*10)/((20*20)+(20*20)-(10*10))
    overlap = boxoverlap(boxa, boxb)
    np.testing.assert_allclose(overlap, expected_overlap, atol=1e-12)