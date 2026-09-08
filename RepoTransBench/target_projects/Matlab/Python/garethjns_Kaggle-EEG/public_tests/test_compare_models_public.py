import pytest
from src.eeg_kaggle.compare_models import compare_models

def test_weighted_mean_aucs_with_different_data():
    SVMs = []
    RBTs = []
    for i in range(3):
        if i % 2 == 0:
            SVMs.append({
                'cvType': 'Custom',
                'AUCScore': 0.91 + (i+1)*0.003,
                'trainedData': [{}]*(12 + i + 1)
            })
            RBTs.append({
                'cvType': 'MATLAB',
                'AUCScore': 0.83 + (i+1)*0.004,
                'cv': {'NumObservations': 20 + (i+1)}
            })
        else:
            SVMs.append({
                'cvType': 'MATLAB',
                'AUCScore': 0.92 + (i+1)*0.002,
                'cv': {'NumObservations': 14 + (i+1)}
            })
            RBTs.append({
                'cvType': 'Custom',
                'AUCScore': 0.82 + (i+1)*0.003,
                'trainedData': [{}]*(16 + (i+1))
            })
    SVMg = {'AUCScore': 0.9342}
    RBTg = {'AUCScore': 0.8497}
    params = {}
    # Expecting only that it does not throw an error and prints something
    compare_models(SVMs, SVMg, RBTs, RBTg, params)