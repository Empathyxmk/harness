import sys
import os

import numpy as np
import pandas as pd
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from timeseriescv.cross_validation import PurgedWalkForwardCV, embargo, BaseTimeSeriesCrossValidator

def test_purged_walk_forward_cv_nondefault_public():
    # Using 'train_length' and 'test_length' as in the source, with different values than private
    df = pd.DataFrame({'value': np.arange(40, 70)})
    splits = []
    cv = PurgedWalkForwardCV(n_splits=5, train_length=6, test_length=2, lookahead=1)
    for train_idx, test_idx in cv.split(df):
        splits.append((train_idx.copy(), test_idx.copy()))
    # Use different assertion checks for public
    assert len(splits) == 5
    assert splits[0][0][0] == 0
    assert splits[-1][1][-1] == df.shape[0] - 1

def test_embargo_public():
    arr = np.zeros(20, dtype=bool)
    embargo(arr, 6, 13, 4)
    # 13,14,15,16 should be embargoed
    assert np.all(arr[13:17])
    assert not arr[12]

def test_walkforward_length_public():
    X = pd.DataFrame({'a': range(30, 64)})
    cv = PurgedWalkForwardCV(n_splits=2, train_length=12, test_length=9, lookahead=2)
    splits = list(cv.split(X))
    assert len(splits) == 2
    # test indices are non-overlapping
    last = -1
    for split in splits:
        assert split[1][0] > last
        last = split[1][-1]

def test_repr_public():
    cv = PurgedWalkForwardCV(n_splits=3, train_length=8, test_length=3, lookahead=3)
    rp = repr(cv)
    assert "PurgedWalkForwardCV" in rp and "n_splits=3" in rp

def test_cross_validator_base_public():
    class DummyCV(BaseTimeSeriesCrossValidator):
        def split(self, X, y=None, pred_times=None, eval_times=None):
            n = len(X)
            yield np.arange(n//3), np.arange(n//3, n//2)
        def get_n_splits(self, X=None, y=None, pred_times=None, eval_times=None):
            return 1

    X = pd.DataFrame({"test": range(10)})
    splits = list(DummyCV().split(X))
    assert len(splits) == 1
    train_idx, test_idx = splits[0]
    assert len(train_idx)
    assert len(test_idx)
    assert set(train_idx).isdisjoint(set(test_idx))

def test_purgedwalkforwardcv_get_n_splits_public():
    df = pd.DataFrame({'col1': np.arange(30, 59)})
    cv = PurgedWalkForwardCV(n_splits=3, train_length=7, test_length=2, lookahead=2)
    assert cv.get_n_splits(df) == 3

def test_split_indices_non_overlap_public():
    df = pd.DataFrame({'v': range(70, 94)})
    cv = PurgedWalkForwardCV(n_splits=4, train_length=5, test_length=5, lookahead=3)
    for tr, te in cv.split(df):
        assert set(tr).isdisjoint(te)

def test_large_embargo_edge_public():
    mask = np.zeros(12, dtype=bool)
    embargo(mask, 8, 10, 4)  # embargo should not go out of bounds
    assert np.all(mask[10:])