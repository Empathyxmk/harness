import pytest
import numpy as np
from src.eeg_kaggle.cv_part import cv_part

def test_basic_partitioning():
    labels = np.array([0]*50 + [1]*50)
    params = {'n_folds': 5}
    cv_obj = cv_part(labels, params)
    assert hasattr(cv_obj, 'train_idx')
    assert hasattr(cv_obj, 'test_idx')
    assert len(cv_obj.train_idx) == params['n_folds']
    assert len(cv_obj.test_idx) == params['n_folds']

    for i in range(params['n_folds']):
        intersection = set(cv_obj.train_idx[i]) & set(cv_obj.test_idx[i])
        assert len(intersection) == 0
        combined_indices = np.unique(np.concatenate([cv_obj.train_idx[i], cv_obj.test_idx[i]]))
        assert np.array_equal(np.sort(combined_indices), np.arange(len(labels)))

    all_test_indices = np.concatenate(cv_obj.test_idx)
    assert np.array_equal(np.sort(all_test_indices), np.arange(len(labels)))

def test_uneven_folds():
    labels = np.array([0]*45 + [1]*55)
    params = {'n_folds': 3}
    cv_obj = cv_part(labels, params)
    assert len(cv_obj.train_idx) == params['n_folds']
    assert len(cv_obj.test_idx) == params['n_folds']
    for i in range(params['n_folds']):
        intersection = set(cv_obj.train_idx[i]) & set(cv_obj.test_idx[i])
        assert len(intersection) == 0
        combined_indices = np.unique(np.concatenate([cv_obj.train_idx[i], cv_obj.test_idx[i]]))
        assert np.array_equal(np.sort(combined_indices), np.arange(len(labels)))

def test_single_fold():
    labels = np.array([0]*10 + [1]*10)
    params = {'n_folds': 1}
    cv_obj = cv_part(labels, params)
    assert len(cv_obj.train_idx) == 1
    assert len(cv_obj.test_idx) == 1
    assert len(cv_obj.train_idx[0]) == 0
    assert np.array_equal(np.sort(cv_obj.test_idx[0]), np.arange(len(labels)))

def test_edge_case_small_data():
    labels = np.array([0, 1])
    params = {'n_folds': 2}
    cv_obj = cv_part(labels, params)
    assert hasattr(cv_obj, 'train_idx') and hasattr(cv_obj, 'test_idx') and len(cv_obj.train_idx) == 2

def test_edge_case_all_same_label():
    labels = np.zeros(10, dtype=int)
    params = {'n_folds': 5}
    cv_obj = cv_part(labels, params)
    assert hasattr(cv_obj, 'train_idx') and hasattr(cv_obj, 'test_idx')