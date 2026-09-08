import numpy as np
import pytest

from bewimm_kinodynamic_rrt_star.init_quad import init_quad
from bewimm_kinodynamic_rrt_star.rrtstar import RRTStar
from bewimm_kinodynamic_rrt_star.quad_is_state_free import quad_is_state_free
from bewimm_kinodynamic_rrt_star.quad_sample_free_states import quad_sample_free_states
from bewimm_kinodynamic_rrt_star.quad_plot_field import quad_plot_field
from bewimm_kinodynamic_rrt_star.is_input_free import is_input_free

def test_public_rrt_quad():
    # Public test case for the quad RRT, based on the MATLAB public test

    # Initialize quad variables
    quad_params = init_quad()
    w = quad_params['w']
    h = quad_params['h']
    d = quad_params['d']
    m = quad_params['m']
    A = quad_params['A']
    B = quad_params['B']
    c = quad_params['c']
    R = quad_params['R']

    quad_radius = max([w,h,d])

    # Limits (see Matlab public_rrt_quad_test.m)
    state_limits = np.array([
        [-2e5,2e5],
        [-2e5,2e5],
        [0,2e5],
        [-2e5,2e5],
        [-2e5,2e5],
        [-2e5,2e5],
        [-2e5,2e5],
        [-2e5,2e5],
        [-2e5,2e5],
        [-2e5,2e5],
    ])
    sampling_limits = np.array([
        [-20,20],
        [5,35],
        [0.5,6],
        [-8,8],
        [-8,8],
        [-8,8],
        [-2,2],
        [-2,2],
        [-8,8],
        [-8,8],
    ])
    input_limits = np.array([
        [-6,8.5],
        [-5,5],
        [-5,5]
    ])

    # Obstacles & waypoints
    obstacles = np.array([[10,10,1,4,4,4]])
    waypoints = np.array([
        [16,36,2.5],
        [2,7,1.5]
    ])
    # z-up convention, flip sign for z
    obstacles[:,2] = -obstacles[:,2]
    waypoints[:,2] = -waypoints[:,2]

    waypoint_states = np.vstack([
        np.hstack([np.array([5,7,1]), np.zeros(7)]),
        np.hstack([waypoints[0], np.zeros(7)]),
        np.hstack([waypoints[1], np.zeros(7)])
    ])
    # Set the columns 4-10 to zero (already in that format)

    # Build the RRTStar instance (assume compatible Python class exists)
    rrt = RRTStar(A,B,c,R,np.arange(3))  # goal dims are 0-based: [0,1,2] for x,y,z

    state_free = lambda state, time_range: quad_is_state_free(state, state_limits, obstacles, quad_radius, time_range)
    input_free = lambda input, time_range: is_input_free(input, input_limits, time_range)
    sample_state = lambda: quad_sample_free_states(sampling_limits, state_limits, obstacles, quad_radius)
    display = lambda scratch, obj, tree, parents, goal, goal_cost, goal_parent: quad_plot_field(scratch, obj, tree, parents, obstacles, waypoints, goal, goal_cost, goal_parent)

    # In the public test: tighter computation limits
    rrt.set_termination_conditions(6000,3)

    # Simulate timer
    # Find path
    path, time = rrt.find_path(sample_state, state_free, input_free, waypoint_states.T, display, 0.5)
    assert path is not None and len(path) > 0, "[PUBLIC TEST] RRT path not found."
    assert time > 0, "[PUBLIC TEST] Computed path should take positive time."