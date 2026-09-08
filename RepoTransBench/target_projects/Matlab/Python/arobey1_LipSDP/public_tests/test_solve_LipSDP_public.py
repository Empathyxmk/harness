import pytest
import numpy as np
from src.lipsdp.solve_sdp import solve_LipSDP

def test_no_split_public(monkeypatch):
    monkeypatch.setattr('src.lipsdp.lipschitz_multi_layer.lipschitz_multi_layer', lambda w, m, v, nr, nd, ndim, net: 11)
    monkeypatch.setattr('src.lipsdp.weight_utils.load_weights', lambda p: ([[np.eye(3)]], [3,3]))
    net = {'alpha': 0.3, 'beta': 2, 'weight_path': ['another_dummy.mat']}
    params = {'formulation': 'network', 'split': False, 'parallel': False, 'verbose': False,
              'split_size': 2, 'num_neurons': 2, 'num_workers': 1, 'num_dec_vars': 2}
    L = solve_LipSDP(net, params)
    assert L == 11

def test_with_split_public(monkeypatch):
    monkeypatch.setattr('src.lipsdp.split_and_solve.split_and_solve', lambda a, b, c, d: 13)
    monkeypatch.setattr('src.lipsdp.weight_utils.split_weights', lambda w, s, d: ([[np.eye(3)], [np.eye(3)]], [[3,3],[3,3]]))
    monkeypatch.setattr('src.lipsdp.weight_utils.load_weights', lambda p: ([[np.eye(3)]], [3,3]))
    net = {'alpha': 0.5, 'beta': 2, 'weight_path': ['public_dummy.mat']}
    params = {'formulation': 'network', 'split': True, 'parallel': False, 'verbose': False,
              'split_size': 2, 'num_neurons': 3, 'num_workers': 1, 'num_dec_vars': 3}
    L = solve_LipSDP(net, params)
    assert L == 13