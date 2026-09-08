import numpy as np
from lihongbo_consensus.helpers import DynamicWindowApproach

def test_public_DynamicWindowApproach():
    x = np.array([5, 5, np.pi/3])
    v = np.array([0.8, 0.2])
    config = {
        'max_speed': 1.5, 'min_speed': 0.05, 'max_yawrate': 3.0,
        'max_accel': 1.0, 'max_dyawrate': 3.5, 'v_reso': 0.02, 'yawrate_reso': 0.02,
        'dt': 0.05, 'predict_time': 2.5, 'to_goal_cost_gain': 1.5, 'speed_cost_gain': 2.0,
        'ob': []
    }
    DynamicWindowApproach(x, v, config=config)