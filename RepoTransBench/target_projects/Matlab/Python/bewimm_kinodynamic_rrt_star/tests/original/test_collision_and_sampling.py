import numpy as np
import pytest

from bewimm_kinodynamic_rrt_star.ball_is_state_free import ball_is_state_free
from bewimm_kinodynamic_rrt_star.ball_sample_free_states import ball_sample_free_states
from bewimm_kinodynamic_rrt_star.quad_is_state_free import quad_is_state_free
from bewimm_kinodynamic_rrt_star.quad_sample_free_states import quad_sample_free_states

# You must supply actual .npy files for obstacles for full functionality. Replace loads below for true test.

@pytest.fixture(scope="module")
def obstacles():
    # Dummy example: array([[1,2,0.5],[3,4,0.6]])
    # Replace with np.load('tests/data/obstacles.npy')
    return np.array([[0,0,1],[3,4,2]])

class TestCollisionAndSampling:
    def test_ball_is_state_free_free(self, obstacles):
        x = np.array([0,0])
        is_free = ball_is_state_free(x, obstacles)
        assert is_free

    def test_ball_is_state_free_collision(self, obstacles):
        obs_center = obstacles[0,0:2]
        obs_radius = obstacles[0,2]
        x_collision = obs_center + np.array([obs_radius/2, 0])
        is_free = ball_is_state_free(x_collision, obstacles)
        assert not is_free

    def test_ball_is_state_free_boundary(self, obstacles):
        obs_center = obstacles[0,0:2]
        obs_radius = obstacles[0,2]
        x_boundary = obs_center + np.array([obs_radius, 0])
        is_free = ball_is_state_free(x_boundary, obstacles)
        assert not is_free

    def test_ball_is_state_free_empty_obstacles(self):
        x = np.array([1,1])
        is_free = ball_is_state_free(x, np.empty((0,3)))
        assert is_free

    def test_quad_is_state_free_free(self, obstacles):
        x = np.zeros(12)
        is_free = quad_is_state_free(x, obstacles)
        assert is_free

    def test_quad_is_state_free_collision(self, obstacles):
        obs_center = obstacles[0,0:2]
        obs_radius = obstacles[0,2]
        x_collision = np.zeros(12)
        x_collision[:2] = obs_center + np.array([obs_radius/2, 0])
        is_free = quad_is_state_free(x_collision, obstacles)
        assert not is_free

    def test_quad_is_state_free_empty_obstacles(self):
        x = np.zeros(12)
        is_free = quad_is_state_free(x, np.empty((0,3)))
        assert is_free

    def test_ball_sample_free_states_output_dimensions(self, obstacles):
        max_val = 10
        min_val = -10
        num_samples = 5
        samples = ball_sample_free_states(num_samples, obstacles, max_val, min_val)
        assert samples.shape == (2, num_samples)

    def test_ball_sample_free_states_are_free(self, obstacles):
        max_val = 10
        min_val = -10
        num_samples = 10
        samples = ball_sample_free_states(num_samples, obstacles, max_val, min_val)
        for i in range(num_samples):
            assert ball_is_state_free(samples[:,i], obstacles)

    def test_ball_sample_free_states_within_bounds(self, obstacles):
        max_val = 10
        min_val = -10
        num_samples = 10
        samples = ball_sample_free_states(num_samples, obstacles, max_val, min_val)
        assert np.all((samples >= min_val) & (samples <= max_val))

    def test_quad_sample_free_states_output_dimensions(self, obstacles):
        max_val = 10
        min_val = -10
        num_samples = 5
        samples = quad_sample_free_states(num_samples, obstacles, max_val, min_val)
        assert samples.shape == (12, num_samples)

    def test_quad_sample_free_states_are_free(self, obstacles):
        max_val = 10
        min_val = -10
        num_samples = 10
        samples = quad_sample_free_states(num_samples, obstacles, max_val, min_val)
        for i in range(num_samples):
            assert quad_is_state_free(samples[:,i], obstacles)

    def test_quad_sample_free_states_position_within_bounds(self, obstacles):
        max_val = 10
        min_val = -10
        num_samples = 10
        samples = quad_sample_free_states(num_samples, obstacles, max_val, min_val)
        assert np.all((samples[0:3,:] >= min_val) & (samples[0:3,:] <= max_val))