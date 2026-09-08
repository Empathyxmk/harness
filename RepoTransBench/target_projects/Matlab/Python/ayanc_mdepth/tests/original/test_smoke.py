import pytest

from src.ayanc_mdepth.consensus import consensus
from src.ayanc_mdepth.loadModel import loadModel

def test_everything_loads():
    # Just checks if main functions can be called without error
    try:
        out1 = consensus([1, 0, 1], [0.1, 0.3, 0.5])
        out2 = loadModel('training/filters_init.caffemodel.h5')
        success = True
    except Exception:
        success = False
    assert success, "Consensus or loadModel callable produced error"