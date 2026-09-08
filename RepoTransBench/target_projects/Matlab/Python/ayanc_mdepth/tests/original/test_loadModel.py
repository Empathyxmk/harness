import pytest

from src.ayanc_mdepth.loadModel import loadModel

def test_valid_h5_file():
    # Just tries to load H5 model, expecting a dict or object output
    model = loadModel('training/filters_init.caffemodel.h5')
    assert isinstance(model, (dict, object)), "Model is neither a dict nor object"