import pytest
import numpy as np
from src.eeg_kaggle.features_object import FeaturesObject

def test_features_object_create_public():
    data = np.random.randn(40, 4)
    params = {}
    params['Fs'] = 512
    params['nChans'] = 4
    params['HillsBands'] = {'Range': list(range(2, 13))}
    obj = FeaturesObject(data, params)
    assert obj.nChans == 4
    assert obj.Fs == 512