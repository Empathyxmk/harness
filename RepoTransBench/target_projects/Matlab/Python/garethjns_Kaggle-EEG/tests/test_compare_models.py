import pytest
import io
import sys
from src.eeg_kaggle.compare_models import compare_models

def test_matlab_cv_type():
    # Structure as per Matlab test
    SVMs_matlab = [
        {'AUCScore': 0.8, 'cvType': 'MATLAB', 'cv': {'NumObservations': 100}},
        {'AUCScore': 0.9, 'cvType': 'MATLAB', 'cv': {'NumObservations': 200}}
    ]
    SVMg_matlab = {'AUCScore': 0.85}

    RBTs_matlab = [
        {'AUCScore': 0.75, 'cvType': 'MATLAB', 'cv': {'NumObservations': 150}},
        {'AUCScore': 0.85, 'cvType': 'MATLAB', 'cv': {'NumObservations': 250}}
    ]
    RBTg_matlab = {'AUCScore': 0.80}

    params = {}

    buf = io.StringIO()
    sys.stdout = buf
    compare_models(SVMs_matlab, SVMg_matlab, RBTs_matlab, RBTg_matlab, params)
    actual_output = buf.getvalue()
    sys.stdout = sys.__stdout__

    assert "SVM: Mean individual AUC: 0.8667 vs general model AUC: 0.85" in actual_output
    assert "RBT: Mean individual AUC: 0.8125 vs general model AUC: 0.8" in actual_output

def test_custom_cv_type():
    SVMs_custom = [
        {'AUCScore': 0.7, 'cvType': 'Custom', 'trainedData': [{}]*50},  # Dummy list to represent 50 obs
        {'AUCScore': 0.75, 'cvType': 'Custom', 'trainedData': [{}]*150}
    ]
    SVMg_custom = {'AUCScore': 0.72}

    RBTs_custom = [
        {'AUCScore': 0.65, 'cvType': 'Custom', 'trainedData': [{}]*70},
        {'AUCScore': 0.70, 'cvType': 'Custom', 'trainedData': [{}]*130}
    ]
    RBTg_custom = {'AUCScore': 0.68}

    params = {}

    buf = io.StringIO()
    sys.stdout = buf
    compare_models(SVMs_custom, SVMg_custom, RBTs_custom, RBTg_custom, params)
    actual_output = buf.getvalue()
    sys.stdout = sys.__stdout__

    assert "SVM: Mean individual AUC: 0.7375 vs general model AUC: 0.72" in actual_output
    assert "RBT: Mean individual AUC: 0.6825 vs general model AUC: 0.68" in actual_output

def test_mixed_cv_type():
    SVMs_mixed = [
        {'AUCScore': 0.8, 'cvType': 'MATLAB', 'cv': {'NumObservations': 100}, 'trainedData': []},
        {'AUCScore': 0.7, 'cvType': 'Custom', 'cv': {'NumObservations': 0}, 'trainedData': [{}]*50}
    ]
    SVMg_mixed = {'AUCScore': 0.75}

    RBTs_mixed = [
        {'AUCScore': 0.9, 'cvType': 'Custom', 'trainedData': [{}]*200, 'cv': {'NumObservations': 0}},
        {'AUCScore': 0.6, 'cvType': 'MATLAB', 'trainedData': [], 'cv': {'NumObservations': 100}}
    ]
    RBTg_mixed = {'AUCScore': 0.8}

    params = {}

    buf = io.StringIO()
    sys.stdout = buf
    compare_models(SVMs_mixed, SVMg_mixed, RBTs_mixed, RBTg_mixed, params)
    actual_output = buf.getvalue()
    sys.stdout = sys.__stdout__

    assert "SVM: Mean individual AUC: 0.7667 vs general model AUC: 0.75" in actual_output
    assert "RBT: Mean individual AUC: 0.8 vs general model AUC: 0.8" in actual_output