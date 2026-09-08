import pytest
import numpy as np
from src.lipsdp import solve_sdp
from src.lipsdp.solve_sdp import solve_LipSDP

def test_no_split(monkeypatch):
    # Patch lipschitz_multi_layer
    monkeypatch.setattr('src.lipsdp.lipschitz_multi_layer.lipschitz_multi_layer', lambda w, m, v, nr, nd, ndim, net: 7)
    # Patch load_weights
    monkeypatch.setattr('src.lipsdp.weight_utils.load_weights', lambda p: ([[np.eye(2)]], [2,2]))
    net = {'alpha': 0.1, 'beta': 1, 'weight_path': ['dummy.mat']}
    params = {'formulation': 'network', 'split': False, 'parallel': False, 'verbose': False,
              'split_size': 1, 'num_neurons': 1, 'num_workers': 1, 'num_dec_vars': 1}
    L = solve_LipSDP(net, params)
    assert L == 7

def test_with_split(monkeypatch):
    # Patch split_and_solve
    monkeypatch.setattr('src.lipsdp.split_and_solve.split_and_solve', lambda a, b, c, d: 9)
    # Patch load_weights and split_weights
    monkeypatch.setattr('src.lipsdp.weight_utils.split_weights', lambda w, s, d: ([[np.eye(2)], [np.eye(2)]], [[2,2],[2,2]]))
    monkeypatch.setattr('src.lipsdp.weight_utils.load_weights', lambda p: ([[np.eye(2)]], [2,2]))
    net = {'alpha': 0.1, 'beta': 1, 'weight_path': ['dummy.mat']}
    params = {'formulation': 'network', 'split': True, 'parallel': False, 'verbose': False,
              'split_size': 1, 'num_neurons': 1, 'num_workers': 1, 'num_dec_vars': 1}
    L = solve_LipSDP(net, params)
    assert L == 9