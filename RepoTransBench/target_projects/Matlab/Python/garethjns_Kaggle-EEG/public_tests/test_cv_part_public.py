import pytest
import numpy as np
from src.eeg_kaggle.cv_part import cv_part

def test_cv_part_basic_public():
    y = np.array([2, 3, 2, 3, 2, 3])
    n_folds = 2
    cvp = cv_part(y, {'n_folds': n_folds})

    assert hasattr(cvp, 'n_folds') and cvp.n_folds == n_folds
    assert set(np.unique(cvp.Y)) == set([2, 3])