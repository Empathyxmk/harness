import pytest
from src.eeg_kaggle.set_params import set_params

def test_default_params():
    initial_params = dict()
    params = set_params(initial_params)

    assert params['Fs'] == 400, 'Fs should be 400'
    assert params['nChans'] == 16, 'nChans should be 16'
    assert params['trainSubs'] == ['1', '2', '3'], "trainSubs should be ['1', '2', '3']"
    assert params['testSubs'] == ['1', '2', '3'], "testSubs should be ['1', '2', '3']"
    assert params['OKThresh'] == 0.5, 'OKThresh should be 0.5'
    assert list(params['HillsBands']['Range']) == list(range(1, 48)), 'HillsBands.Range should be 1:47 (inclusive)'

def test_existing_params_are_preserved():
    initial_params = {'someOtherField': 'value'}
    params = set_params(initial_params)
    assert params['someOtherField'] == 'value', 'Existing fields should be preserved'
    assert params['Fs'] == 400, 'Fs should still be set to its default'