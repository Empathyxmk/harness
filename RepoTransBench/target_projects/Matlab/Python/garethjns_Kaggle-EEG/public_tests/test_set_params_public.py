import pytest
from src.eeg_kaggle.set_params import set_params

def test_set_params_different_input():
    params = {'trainSubs': ['5', '6'], 'testSubs': ['5', '6']}
    params = set_params(params)

    assert params['Fs'] == 400
    assert params['nChans'] == 16
    assert 'HillsBands' in params
    assert params['trainSubs'] == ['1', '2', '3'], "trainSubs should be overwritten to default list"