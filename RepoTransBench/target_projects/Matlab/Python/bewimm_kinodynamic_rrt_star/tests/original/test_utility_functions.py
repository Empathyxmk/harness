import numpy as np
import pytest

from bewimm_kinodynamic_rrt_star.is_positive_definite import is_positive_definite
from bewimm_kinodynamic_rrt_star.is_input_free import is_input_free

class TestUtilityFunctions:
    def test_is_positive_definite_true(self):
        A = np.array([[2, -1], [-1, 2]])
        assert is_positive_definite(A)
        assert is_positive_definite(np.eye(3))
    def test_is_positive_definite_false_not_symmetric(self):
        A = np.array([[1,2],[0,1]])
        assert not is_positive_definite(A)
    def test_is_positive_definite_false_not_positive(self):
        A = np.array([[-2,-1],[-1,-2]])
        assert not is_positive_definite(A)
        A = np.array([[1,1],[1,1]])
        assert not is_positive_definite(A)
    def test_is_positive_definite_false_non_square(self):
        A = np.array([[1,2,3],[4,5,6]])
        assert not is_positive_definite(A)
    def test_is_positive_definite_false_empty_matrix(self):
        A = np.empty((0,0))
        assert not is_positive_definite(A)
    def test_is_input_free_valid_input(self):
        u_valid = np.array([1,2,3])
        assert is_input_free(u_valid)
    def test_is_input_free_nan(self):
        u_nan = np.array([1,np.nan,3])
        assert not is_input_free(u_nan)
    def test_is_input_free_inf(self):
        u_inf = np.array([1,np.inf,3])
        assert not is_input_free(u_inf)
        u_neg_inf = np.array([1,-np.inf,3])
        assert not is_input_free(u_neg_inf)
    def test_is_input_free_empty(self):
        u_empty = np.array([])
        assert is_input_free(u_empty)
    def test_is_input_free_all_valid(self):
        u = np.random.rand(4)
        assert is_input_free(u)