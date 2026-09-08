import numpy as np
from src.lipsdp.lipschitz_multi_layer import lipschitz_multi_layer

def test_modes():
    # 'network', 'network-rand', 'network-dec-vars', 'neuron', 'layer'
    make_net = lambda N: {'alpha':0.1,'beta':1.0,'weight_path':['dummy']}
    w = [[np.eye(3), np.eye(3), np.eye(3)]]
    net_dims = [3,3,3,3]
    # 'network'
    try:
        lipschitz_multi_layer(w, 'network', False, 2, 2, net_dims, make_net(3))
    except Exception:
        pass
    # 'network-rand', input > nchoosek(N,2)
    try:
        lipschitz_multi_layer(w, 'network-rand', False, 20, 2, net_dims, make_net(3))
    except:
        pass
    # 'network-dec-vars', input > nchoosek(N,2)
    try:
        lipschitz_multi_layer(w, 'network-dec-vars', False, 2, 20, net_dims, make_net(3))
    except:
        pass
    # 'neuron'
    try:
        lipschitz_multi_layer(w, 'neuron', False, 2, 2, net_dims, make_net(3))
    except:
        pass
    # 'layer'
    try:
        lipschitz_multi_layer(w, 'layer', False, 2, 2, net_dims, make_net(3))
    except:
        pass