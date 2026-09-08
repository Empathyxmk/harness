import numpy as np
from lihongbo_consensus.helpers import DynamicWindowApproach

def test_DynamicWindowApproach_basic():
    x = np.array([0, 0, 0, 0])
    v = np.array([0, 0])
    Vr = np.array([[0, 1], [-0.5, 0.5]])
    u = np.array([1, 0])
    ob = np.array([])
    config = {
        'max_speed': 1, 'min_speed': -0.5, 'max_yawrate': 1.0, 'max_accel': 0.2,
        'v_reso': 0.1, 'yawrate_reso': 0.1,
        'dt': 0.1, 'predict_time': 1.0, 'to_goal_cost_gain': 1.0,
        'speed_cost_gain': 1.0, 'obstacle_cost_gain': 1.0
    }
    vopt, trajectory = DynamicWindowApproach(x, v, Vr, u, ob, config)
    assert vopt.shape == (2,)
    assert trajectory.shape[1] == int(config['predict_time'] / config['dt']) + 1

    # Edge: obstacles present
    ob2 = np.array([[1, 1]])
    vopt2, _ = DynamicWindowApproach(x, v, Vr, u, ob2, config)
    assert vopt2.shape == (2,)