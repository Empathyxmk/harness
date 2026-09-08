import sys
import os

import numpy as np
import pandas as pd
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from timeseriescv.cross_validation import BaseTimeSeriesCrossValidator, PurgedWalkForwardCV

def test_errors_n_splits_public():
    df = pd.DataFrame(np.zeros((15, 1)))
    with pytest.raises(ValueError):
        PurgedWalkForwardCV(n_splits=16, train_length=1, test_length=1, lookahead=0).split(df).__next__()

def test_errors_train_length_public():
    df = pd.DataFrame(np.zeros((12, 1)))
    with pytest.raises(ValueError):
        PurgedWalkForwardCV(n_splits=3, train_length=11, test_length=2, lookahead=0).split(df).__next__()

def test_errors_test_length_public():
    df = pd.DataFrame(np.zeros((10, 1)))
    with pytest.raises(ValueError):
        PurgedWalkForwardCV(n_splits=2, train_length=2, test_length=9, lookahead=0).split(df).__next__()

def test_errors_lookahead_negative_public():
    with pytest.raises(ValueError):
        PurgedWalkForwardCV(n_splits=2, train_length=2, test_length=2, lookahead=-4)

def test_basecv_split_signature_public():
    # split method not implemented
    class DummyCV(BaseTimeSeriesCrossValidator):
        def get_n_splits(self, X=None, y=None, pred_times=None, eval_times=None):
            return 1

    df = pd.DataFrame(np.zeros((4, 1)))
    with pytest.raises(TypeError):
        DummyCV().split(df)