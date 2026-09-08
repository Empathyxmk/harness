import pytest

from src.ayanc_mdepth.loadModel import loadModel

def test_valid_h5_file():
    model = loadModel('training/filters_init.caffemodel.h5')
    assert model is not None, "Loaded model is empty"