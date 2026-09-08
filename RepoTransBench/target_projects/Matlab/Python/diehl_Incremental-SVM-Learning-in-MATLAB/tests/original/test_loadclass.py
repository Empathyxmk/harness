import os
import numpy as np

# Replace with your real saveclass/loadclass Python functions!
def saveclass(filename, data):
    np.savetxt(filename, data, fmt='%d')

def loadclass(filename):
    return np.loadtxt(filename, dtype=int)

def test_loadclass_basic(tmp_path):
    filename = tmp_path / "testclass_tmp.txt"
    data = np.array([-1, 1, -1, 1, 1])
    saveclass(filename, data)
    loaded = loadclass(filename)
    assert np.array_equal(data, loaded)
    os.remove(filename)