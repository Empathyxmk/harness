import numpy as np
from src.lipsdp.split_and_solve import split_and_solve

def test_single_matrix():
    split_W = [[np.eye(2)]]
    split_net_dims = [[2,2]]
    network = {'alpha': 0.1, 'beta': 1.0, 'weight_path': ['dummy']}
    lip_params = {'formulation':'layer','split':False,'parallel':False,
                  'verbose':False,'split_size':1,'num_neurons':1,'num_workers':1,'num_dec_vars':1}
    value = split_and_solve(split_W, split_net_dims, lip_params, network)
    assert value == 1

def test_multi_matrix(monkeypatch):
    w1 = np.eye(2)
    w2 = 2 * np.eye(2)
    split_W = [[w1, w2]]
    split_net_dims = [[2,2,2]]
    network = {'alpha':0.1,'beta':1.0,'weight_path':['dummy']}
    # Patch lipschitz_multi_layer to return 3
    monkeypatch.setattr('src.lipsdp.lipschitz_multi_layer.lipschitz_multi_layer', lambda *a, **k: 3)
    lip_params = {'formulation':'network','split':False,'parallel':False,
                  'verbose':False,'split_size':1,'num_neurons':1,'num_workers':1,'num_dec_vars':1}
    value = split_and_solve(split_W, split_net_dims, lip_params, network)
    assert value == 3