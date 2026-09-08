import numpy as np
import pytest

from bewimm_kinodynamic_rrt_star.init_quad import init_quad
from bewimm_kinodynamic_rrt_star.is_positive_definite import is_positive_definite
from bewimm_kinodynamic_rrt_star.is_input_free import is_input_free
from bewimm_kinodynamic_rrt_star.double_integrator import double_integrator

class TestCoreUtilities:
    def test_init_quad_output_structure(self):
        params = init_quad()
        assert isinstance(params, dict)
        for field in ['g','m','l','Ixx','Iyy','Izz','kd','km','u_min','u_max']:
            assert field in params
        assert isinstance(params['g'], (int, float))
        assert isinstance(params['m'], (int, float))

    def test_init_quad_parameter_values(self):
        params = init_quad()
        assert params['g'] > 0
        assert params['m'] > 0
        assert params['l'] > 0
        assert np.all(params['u_min'] >= 0)
        assert np.all(params['u_max'] > params['u_min'])

    def test_is_positive_definite_true(self):
        A = np.array([[2, -1], [-1, 2]])
        result = is_positive_definite(A)
        assert result
    def test_is_positive_definite_false_not_symmetric(self):
        A = np.array([[1,2],[0,1]])
        assert not is_positive_definite(A)
    def test_is_positive_definite_false_not_pd(self):
        A = np.array([[1,2],[2,1]])
        assert not is_positive_definite(A)
    def test_is_positive_definite_false_singular(self):
        A = np.array([[1,1],[1,1]])
        assert not is_positive_definite(A)
    def test_is_positive_definite_scalar(self):
        assert is_positive_definite(5)
        assert not is_positive_definite(-5)
        assert not is_positive_definite(0)
    def test_is_positive_definite_non_square(self):
        A = np.array([[1,2,3],[4,5,6]])
        assert not is_positive_definite(A)
    def test_is_input_free_within_bounds(self):
        u = np.array([0.5,0.5,0.5,0.5])
        params = {'u_min': np.zeros(4), 'u_max': np.ones(4)}
        assert is_input_free(u, params)
    def test_is_input_free_at_lower_bound(self):
        u = np.zeros(4)
        params = {'u_min': np.zeros(4), 'u_max': np.ones(4)}
        assert is_input_free(u, params)
    def test_is_input_free_at_upper_bound(self):
        u = np.ones(4)
        params = {'u_min': np.zeros(4), 'u_max': np.ones(4)}
        assert is_input_free(u, params)
    def test_is_input_free_below_lower_bound(self):
        u = np.array([-0.1,0.5,0.5,0.5])
        params = {'u_min': np.zeros(4), 'u_max': np.ones(4)}
        assert not is_input_free(u, params)
    def test_is_input_free_above_upper_bound(self):
        u = np.array([0.5,1.1,0.5,0.5])
        params = {'u_min': np.zeros(4), 'u_max': np.ones(4)}
        assert not is_input_free(u, params)
    def test_is_input_free_mixed_bounds(self):
        u = np.array([0.5,1.1,-0.1,0.5])
        params = {'u_min': np.zeros(4), 'u_max': np.ones(4)}
        assert not is_input_free(u, params)
    def test_double_integrator_zero_input(self):
        x0 = np.array([0,0,0,0])
        u = np.array([0,0])
        dt = 0.1
        xf = double_integrator(x0,u,dt)
        expected_xf = np.array([0+0*dt, 0+0*dt, 0, 0])
        assert np.allclose(xf, expected_xf, atol=1e-9)
    def test_double_integrator_constant_input(self):
        x0 = np.array([0,0,0,0])
        u = np.array([1,0])
        dt = 0.1
        expected_xf = np.array([0+0*dt+0.5*1*dt**2, 0+0*dt+0.5*0*dt**2, 0+1*dt, 0+0*dt])
        xf = double_integrator(x0,u,dt)
        assert np.allclose(xf, expected_xf, atol=1e-9)
    def test_double_integrator_nonzero_initial_velocity(self):
        x0 = np.array([0,0,1,2])
        u = np.array([0,0])
        dt = 0.5
        expected_xf = np.array([x0[0]+x0[2]*dt, x0[1]+x0[3]*dt, x0[2], x0[3]])
        xf = double_integrator(x0,u,dt)
        assert np.allclose(xf, expected_xf, atol=1e-9)