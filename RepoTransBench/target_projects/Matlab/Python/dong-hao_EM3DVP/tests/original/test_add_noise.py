import pytest
import numpy as np
import copy

def add_noise(data, nsite, nlevel):
    # Simulate noise addition on data as in the Matlab logic
    # For each site, add noise to tf and store in tf_o
    data2 = copy.deepcopy(data)
    rng = np.random.default_rng(1234)
    for k in range(nsite):
        tf = data2[k]['tf']
        orig_shape = tf.shape
        if nlevel > 0:
            noise = rng.normal(loc=0.0, scale=nlevel, size=orig_shape)
            data2[k]['tf_o'] = tf * (1 + noise)
        else:
            data2[k]['tf_o'] = data2[k]['tf_o']
    return data2

def test_NoiseAdded():
    data = [{'tf': np.ones((2,2)), 'tf_o': np.ones((2,2))}]
    nsite = 1
    nlevel = 0.2
    data2 = add_noise(data, nsite, nlevel)
    assert not np.allclose(data2[0]['tf_o'], np.ones((2,2))), "tf_o should change with noise"
    assert data2[0]['tf_o'].shape == (2,2)

def test_ZeroNoise():
    tf = np.random.rand(3,4)
    tf_o = np.random.rand(3,4)
    data = [{'tf': tf, 'tf_o': tf_o}]
    nsite = 1
    nlevel = 0.0
    orig = tf_o.copy()
    data2 = add_noise(data, nsite, nlevel)
    assert np.allclose(data2[0]['tf_o'], orig)

def test_MultipleSites():
    data = []
    for k in range(3):
        data.append({'tf': 2*np.ones((2,2)), 'tf_o': 3*np.ones((2,2))})
    nlevel = 0.1
    newdata = add_noise(data, 3, nlevel)
    for i, d in enumerate(newdata):
        assert d['tf_o'].shape == (2,2)
        assert not np.allclose(d['tf_o'], 3*np.ones((2,2))), f'Site {i} tf_o should change with noise'