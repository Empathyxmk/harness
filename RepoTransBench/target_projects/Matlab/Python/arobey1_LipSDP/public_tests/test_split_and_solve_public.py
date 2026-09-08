import numpy as np
import pytest
from src.lipsdp.split_and_solve import split_and_solve

def test_split_and_solve_norm_public():
    split_W = [[np.eye(3)], [np.eye(3)]]
    split_net_dims = [[3,3], [3,3]]
    lip_params = {'formulation': 'layer', 'split': True, 'parallel': False, 
                  'verbose': False, 'split_size': 2, 'num_neurons': 3, 'num_workers': 1, 'num_dec_vars': 2}
    network = {'alpha':0.7, 'beta':1.5, 'weight_path':['split_dummy.mat']}
    assert split_and_solve(split_W, split_net_dims, lip_params, network) == 1

def test_split_and_solve_multi_layer_mock_public(monkeypatch):
    monkeypatch.setattr('src.lipsdp.lipschitz_multi_layer.lipschitz_multi_layer', lambda *a, **k: 5)
    split_W = [ [np.random.rand(3,3), np.random.rand(3,3)], [np.random.rand(3,3), np.random.rand(3,3)] ]
    split_net_dims = [ [3,3,3], [3,3,3] ]
    lip_params = {'formulation': 'network', 'split': True, 'parallel': False,
                  'verbose': False, 'split_size': 2, 'num_neurons': 3, 'num_workers': 1, 'num_dec_vars': 2}
    network = {'alpha':0.2, 'beta':1.1, 'weight_path':['mock_split.mat']}
    assert split_and_solve(split_W, split_net_dims, lip_params, network) == 25