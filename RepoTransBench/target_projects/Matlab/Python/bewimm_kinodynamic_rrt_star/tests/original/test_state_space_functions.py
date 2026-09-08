import numpy as np
import pytest

from bewimm_kinodynamic_rrt_star.quad_is_state_free import quad_is_state_free
from bewimm_kinodynamic_rrt_star.init_quad import init_quad
from bewimm_kinodynamic_rrt_star.ball_is_state_free import ball_is_state_free
from bewimm_kinodynamic_rrt_star.quad_sample_free_states import quad_sample_free_states
from bewimm_kinodynamic_rrt_star.ball_sample_free_states import ball_sample_free_states

class TestStateSpaceFunctions:
    def test_quad_is_state_free_free_space(self):
        # x = [0;0;5] + 9x0
        x = np.zeros(12)
        x[2] = 5
        obstacles = np.array([[100,100,100,1]])
        is_free, r_min = quad_is_state_free(x, None, obstacles)
        assert is_free
        assert r_min > 0

    def test_quad_is_state_free_collision(self):
        x = np.zeros(12)
        quad_params = init_quad()
        r_quad = quad_params['l']/2
        # obstacle at origin
        obstacles = np.array([[0,0,0, r_quad - 0.01]])
        is_free, r_min = quad_is_state_free(x, None, obstacles)
        assert not is_free
        assert r_min == 0
        # nearby collision
        obstacles = np.array([[0.1,0,0, r_quad-0.01]])
        is_free, r_min = quad_is_state_free(x, None, obstacles)
        assert not is_free
        assert r_min == 0

    def test_quad_is_state_free_out_of_bounds(self):
        obstacles = np.empty((0,4))
        # X out of bounds
        x = np.zeros(12)
        x[0] = -11
        is_free, _ = quad_is_state_free(x, None, obstacles)
        assert not is_free
        x[0] = 11
        is_free, _ = quad_is_state_free(x, None, obstacles)
        assert not is_free
        x[0] = 0
        x[1] = -11
        is_free, _ = quad_is_state_free(x, None, obstacles)
        assert not is_free
        x[1] = 11
        is_free, _ = quad_is_state_free(x, None, obstacles)
        assert not is_free
        x[1] = 0
        x[2] = -1
        is_free, _ = quad_is_state_free(x, None, obstacles)
        assert not is_free
        x[2] = 11
        is_free, _ = quad_is_state_free(x, None, obstacles)
        assert not is_free

    def test_quad_is_state_free_multiple_obstacles(self):
        x = np.zeros(12)
        quad_params = init_quad()
        r_quad = quad_params['l']/2
        obstacles = np.array([
            [10,0,0,1],
            [0,0,0, r_quad-0.01],
            [-10,0,0,1]
        ])
        is_free, r_min = quad_is_state_free(x, None, obstacles)
        assert not is_free
        assert r_min == 0

    def test_ball_is_state_free_free_space(self):
        x = np.zeros(4)
        obstacles = np.array([[100,100,1]])
        is_free, r_min = ball_is_state_free(x, None, obstacles)
        assert is_free
        assert r_min > 0

    def test_ball_is_state_free_collision(self):
        x = np.zeros(4)
        r_ball = 0.1
        obstacles = np.array([[0,0, r_ball-0.01]])
        is_free, r_min = ball_is_state_free(x, None, obstacles)
        assert not is_free
        assert r_min == 0
        obstacles = np.array([[0.1,0, r_ball-0.01]])
        is_free, r_min = ball_is_state_free(x, None, obstacles)
        assert not is_free
        assert r_min == 0

    def test_ball_is_state_free_out_of_bounds(self):
        obstacles = np.empty((0,3))
        x = np.array([-11,0,0,0])
        is_free, _ = ball_is_state_free(x, None, obstacles)
        assert not is_free
        x = np.array([11,0,0,0])
        is_free, _ = ball_is_state_free(x, None, obstacles)
        assert not is_free
        x = np.array([0,-11,0,0])
        is_free, _ = ball_is_state_free(x, None, obstacles)
        assert not is_free
        x = np.array([0,11,0,0])
        is_free, _ = ball_is_state_free(x, None, obstacles)
        assert not is_free

    def test_quad_sample_free_states_basic(self):
        num_samples = 5
        start_pos = np.zeros(12)
        goal_pos = np.array([1,1,1] + [0]*9)
        obstacles = np.array([[100,100,100,1]])
        xs = quad_sample_free_states(num_samples, start_pos, goal_pos, obstacles)
        assert xs.shape == (12, num_samples)
        for i in range(num_samples):
            is_free, _ = quad_is_state_free(xs[:,i], None, obstacles)
            assert is_free
            assert np.all(xs[0:3,i] >= np.array([-10,-10,0]))
            assert np.all(xs[0:3,i] <= np.array([10,10,10]))
            assert np.all(xs[3:,i] == 0)

    def test_quad_sample_free_states_collision_avoidance(self):
        num_samples = 10
        start_pos = np.zeros(12)
        goal_pos = np.array([1,1,1] + [0]*9)
        quad_params = init_quad()
        r_quad = quad_params['l']/2
        obstacles = np.array([[0,0,0, r_quad+0.1]])
        xs = quad_sample_free_states(num_samples, start_pos, goal_pos, obstacles)
        assert xs.shape == (12, num_samples)
        for i in range(num_samples):
            is_free, _ = quad_is_state_free(xs[:,i], None, obstacles)
            assert is_free
            d = np.linalg.norm(xs[0:3,i] - obstacles[0,:3])
            assert d > (obstacles[0,3] + r_quad)

    def test_ball_sample_free_states_basic(self):
        num_samples = 5
        start_pos = np.array([0,0,0,0])
        goal_pos = np.array([1,1,0,0])
        obstacles = np.array([[100,100,1]])
        xs = ball_sample_free_states(num_samples, start_pos, goal_pos, obstacles)
        assert xs.shape == (4, num_samples)
        for i in range(num_samples):
            is_free, _ = ball_is_state_free(xs[:,i], None, obstacles)
            assert is_free
            assert np.all(xs[0:2,i] >= np.array([-10,-10]))
            assert np.all(xs[0:2,i] <= np.array([10,10]))
            assert np.all(xs[2:4,i] == 0)

    def test_ball_sample_free_states_collision_avoidance(self):
        num_samples = 10
        start_pos = np.array([0,0,0,0])
        goal_pos = np.array([1,1,0,0])
        r_ball = 0.1
        obstacles = np.array([[0,0, r_ball+0.1]])
        xs = ball_sample_free_states(num_samples, start_pos, goal_pos, obstacles)
        assert xs.shape == (4, num_samples)
        for i in range(num_samples):
            is_free, _ = ball_is_state_free(xs[:,i], None, obstacles)
            assert is_free
            d = np.linalg.norm(xs[0:2,i] - obstacles[0,0:2])
            assert d > obstacles[0,2] + r_ball