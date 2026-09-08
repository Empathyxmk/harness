import pytest
import numpy as np
from src.eeg_kaggle.seizure_model import SeizureModel

def test_seizure_model_basic_fit_public():
    data = np.random.rand(24,6)
    labels = np.array([i%2 for i in range(24)])
    params = {'nChans': 6, 'subject': 'XPublic', 'type': 'publicType'}
    model = SeizureModel(data, labels, params)
    fields = vars(model)
    assert 'AUCScore' in fields or 'trained_model' in fields, 'Fields missing'