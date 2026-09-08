import numpy as np
import pytest

# These tests assume quad_is_state_free and quad_sample_free_states are imported from src

from bewimm_kinodynamic_rrt_star.quad_is_state_free import quad_is_state_free
from bewimm_kinodynamic_rrt_star.quad_sample_free_states import quad_sample_free_states

class TestQuadFunctions:
    @pytest.fixture(autouse=True)
    def setup(self):
        # "StateLimits" and "SampleLimits" as in the Matlab tests
        self.state_limits = np.array([
            [-10, 10], [-10, 10], [-10, 10], 
            [-np.pi, np.pi], [-np.pi, np.pi], [-np.pi, np.pi], 
            [-10, 10], [-10, 10], [-10, 10], [-10, 10]
        ])
        self.sample_limits = np.vstack((
            np.array([[-5, 5], [-5, 5], [-5, 5]]),
            np.tile(np.array([[-np.pi, np.pi]]), (7,1))
        ))
        self.quad_dim = 0.2

    def test_is_state_free_no_obstacles(self):
        state = np.zeros((10,))
        obstacles = np.empty((0,6))
        ok = quad_is_state_free(state, self.state_limits, obstacles, self.quad_dim, [0,0])
        assert ok

    def test_is_state_free_out_of_bounds(self):
        state = self.state_limits[:,0] - 1
        ok = quad_is_state_free(state, self.state_limits, None, self.quad_dim, [0,0])
        assert not ok
        state = self.state_limits[:,1] + 1
        ok = quad_is_state_free(state, self.state_limits, None, self.quad_dim, [0,0])
        assert not ok

    def test_is_state_free_collision_bounding_box(self):
        state = np.array([0.5,0.5,0.5] + [0]*7)
        obstacles = np.array([[0,0,0,1,1,1]])
        ok = quad_is_state_free(state, self.state_limits, obstacles, self.quad_dim, [0,0])
        assert not ok

    def test_is_state_free_collision_radius(self):
        state = np.array([1.1,0.5,0.5] + [0]*7)
        obstacles = np.array([[0,0,0,1,1,1]])
        radius = 0.2
        ok = quad_is_state_free(state, self.state_limits, obstacles, radius, [0,0])
        assert not ok

    def test_is_state_free_no_collision_far_from_obstacle(self):
        state = np.array([2,2,2] + [0]*7)
        obstacles = np.array([[0,0,0,1,1,1]])
        ok = quad_is_state_free(state, self.state_limits, obstacles, self.quad_dim, [0,0])
        assert ok

    def test_is_state_free_multiple_obstacles_collision(self):
        state = np.array([0.5,0.5,0.5] + [0]*7)
        obstacles = np.array([[0,0,0,1,1,1],[10,10,10,1,1,1]])
        ok = quad_is_state_free(state, self.state_limits, obstacles, self.quad_dim, [0,0])
        assert not ok

    def test_is_state_free_multiple_obstacles_no_collision(self):
        state = np.array([5,5,5] + [0]*7)
        obstacles = np.array([[0,0,0,1,1,1],[10,10,10,1,1,1]])
        ok = quad_is_state_free(state, self.state_limits, obstacles, self.quad_dim, [0,0])
        assert ok

    def test_is_state_free_function_handle_no_collision(self):
        test_state_func = lambda t: np.array([t*0.1, t*0.1, t*0.1] + [0.0]*7)
        time_range = [0, 1]
        obstacles = np.array([[1,1,1,0.1,0.1,0.1]])
        ok = quad_is_state_free(test_state_func, self.state_limits, obstacles, self.quad_dim, time_range)
        assert ok

    def test_is_state_free_function_handle_collision(self):
        test_state_func = lambda t: np.array([t, t, t] + [0.0]*7)
        time_range = [0, 1]
        obstacles = np.array([[0.4,0.4,0.4,0.2,0.2,0.2]])
        ok = quad_is_state_free(test_state_func, self.state_limits, obstacles, 0.01, time_range)
        assert not ok

    def test_is_state_free_function_handle_out_of_bounds(self):
        test_state_func = lambda t: np.array([t*100, t, t] + [0.0]*7)
        time_range = [0,0.2]
        obstacles = np.empty((0,6))
        ok = quad_is_state_free(test_state_func, self.state_limits, obstacles, self.quad_dim, time_range)
        assert not ok

    def test_sample_free_states_no_obstacles(self):
        obstacles = np.empty((0,6))
        state = quad_sample_free_states(self.sample_limits, self.state_limits, obstacles, self.quad_dim)
        assert np.all(state >= self.sample_limits[:,0])
        assert np.all(state <= self.sample_limits[:,1])
        is_free = quad_is_state_free(state, self.state_limits, obstacles, self.quad_dim, [0,0])
        assert is_free

    def test_sample_free_states_with_obstacles(self):
        obstacles = np.array([[0,0,0,1,1,1]])
        state = quad_sample_free_states(self.sample_limits, self.state_limits, obstacles, self.quad_dim)
        assert np.all(state >= self.sample_limits[:,0])
        assert np.all(state <= self.sample_limits[:,1])
        is_free = quad_is_state_free(state, self.state_limits, obstacles, self.quad_dim, [0,0])
        assert is_free