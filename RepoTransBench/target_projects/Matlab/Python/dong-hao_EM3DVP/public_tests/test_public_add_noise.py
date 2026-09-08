import pytest
import numpy as np
import copy

def add_noise(data, nsite, nlevel):
    # Simulate Matlab logic for adding noise
    data2 = copy.deepcopy(data)
    rng = np.random.default_rng(4321)
    for k in range(nsite):
        tf = data2[k]['tf']
        orig_shape = tf.shape
        if nlevel > 0:
            noise = rng.normal(loc=0.0, scale=nlevel, size=orig_shape)
            data2[k]['tf_o'] = tf * (1 + noise)
        else:
            data2[k]['tf_o'] = data2[k]['tf_o']
    return data2

def test_NoiseAddedOtherData():
    data = [{'tf': 5*np.ones((4,1)), 'tf_o': 7*np.ones((4,1))}]
    nsite = 1
    nlevel = 0.15
    data2 = add_noise(data, nsite, nlevel)
    assert not np.allclose(data2[0]['tf_o'], 7*np.ones((4,1))), "tf_o should change with noise"
    assert data2[0]['tf_o'].shape == (4,1)

def test_NonzeroNoiseRandomMatrix():
    tf = np.random.rand(5,3)
    tf_o = np.random.rand(5,3)
    data = [{'tf': tf, 'tf_o': tf_o}]
    nsite = 1
    nlevel = 0.05
    orig = tf_o.copy()
    data2 = add_noise(data, nsite, nlevel)
    assert not np.allclose(data2[0]['tf_o'], orig)

def test_NoiseWithLargerMultipleSites():
    data = []
    for k in range(4):
        data.append({'tf': 4*np.ones((2,3)), 'tf_o': 8*np.ones((2,3))})
    nlevel = 0.3
    newdata = add_noise(data, 4, nlevel)
    for i, d in enumerate(newdata):
        assert d['tf_o'].shape == (2,3)
        assert not np.allclose(d['tf_o'], 8*np.ones((2,3))), f'Site {i} tf_o should change with noise'