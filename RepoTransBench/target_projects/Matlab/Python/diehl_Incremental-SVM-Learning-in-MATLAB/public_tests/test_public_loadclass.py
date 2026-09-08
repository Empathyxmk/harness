import os
import numpy as np

def saveclass(filename, data):
    np.savetxt(filename, data, fmt='%d')

def loadclass(filename):
    return np.loadtxt(filename, dtype=int)

def test_public_loadclass(tmp_path):
    filename = tmp_path / "pub_class_tmp.txt"
    data = np.array([1, -1, -1, 1, -1])
    saveclass(filename, data)
    loaded = loadclass(filename)
    assert np.array_equal(data, loaded)
    os.remove(filename)