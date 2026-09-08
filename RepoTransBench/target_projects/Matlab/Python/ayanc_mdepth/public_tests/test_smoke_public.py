import pytest

from src.ayanc_mdepth.consensus import consensus
from src.ayanc_mdepth.loadModel import loadModel

def test_everything_loads():
    try:
        out1 = consensus([0, 1, 0, 1], [1, 2, 3, 4])
        out2 = loadModel('training/filters_init.caffemodel.h5')
        success = True
    except Exception:
        success = False
    assert success, "Consensus or loadModel callable produced error"