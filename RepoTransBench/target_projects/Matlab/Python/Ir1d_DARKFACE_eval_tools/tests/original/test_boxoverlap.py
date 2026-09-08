import numpy as np
import pytest
from py_ir1d_darkface_eval_tools.boxoverlap import boxoverlap

def test_basic_overlap():
    # a = [10 10 20 20; 15 15 25 25]; b = [18 18 28 28]
    a = np.array([[10,10,20,20], [15,15,25,25]])
    b = np.array([18,18,28,28])
    o = boxoverlap(a, b)
    # Derived as in Matlab comments
    expected_o = np.array([9/233, 64/178])
    np.testing.assert_allclose(o, expected_o, atol=1e-6)

def test_no_overlap():
    a = np.array([[10,10,20,20], [30,30,40,40]])
    b = np.array([1,1,5,5])
    o = boxoverlap(a, b)
    np.testing.assert_allclose(o, [0,0])

def test_one_box_contains_another():
    # b is in a
    a = np.array([[10,10,50,50]])
    b = np.array([20,20,30,30])
    o = boxoverlap(a, b)
    expected_o = 121/1681
    np.testing.assert_allclose(o, expected_o, atol=1e-6)
    # a is in b
    a = np.array([[20,20,30,30]])
    b = np.array([10,10,50,50])
    o = boxoverlap(a, b)
    expected_o = 121/1681
    np.testing.assert_allclose(o, expected_o, atol=1e-6)

def test_identical_boxes():
    a = np.array([[10,10,20,20]])
    b = np.array([10,10,20,20])
    o = boxoverlap(a, b)
    assert o == 1

def test_zero_area_boxes():
    # a zero width
    a = np.array([[10,10,10,20]])
    b = np.array([10,10,20,20])
    o = boxoverlap(a, b)
    assert o == 0
    # a zero height
    a = np.array([[10,10,20,10]])
    b = np.array([10,10,20,20])
    o = boxoverlap(a, b)
    assert o == 0
    # b zero width
    a = np.array([[10,10,20,20]])
    b = np.array([10,10,10,20])
    o = boxoverlap(a, b)
    assert o == 0
    # b zero height
    a = np.array([[10,10,20,20]])
    b = np.array([10,10,20,10])
    o = boxoverlap(a, b)
    assert o == 0

def test_empty_a():
    a = np.zeros((0,4))
    b = np.array([10,10,20,20])
    o = boxoverlap(a, b)
    assert o.shape == (0,1)