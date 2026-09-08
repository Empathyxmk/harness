import pytest
import pandas as pd
import numpy as np

from timeseriescv.cross_validation import BaseTimeSeriesCrossValidator, PurgedWalkForwardCV

class DummyCV(BaseTimeSeriesCrossValidator):
    def split(self, X: pd.DataFrame, y: pd.Series = None, pred_times: pd.Series = None, eval_times: pd.Series = None):
        return super().split(X, y, pred_times, eval_times)


def test_n_splits_type():
    with pytest.raises(ValueError, match="Integral"):
        BaseTimeSeriesCrossValidator(n_splits="not_an_int")


def test_n_splits_too_low():
    with pytest.raises(ValueError, match="n_splits = 2 or more"):
        BaseTimeSeriesCrossValidator(n_splits=1)


def test_split_invalid_X_type():
    cv = DummyCV(n_splits=2)
    with pytest.raises(ValueError, match="X should be a pandas DataFrame/Series"):
        cv.split([1, 2, 3], y=None, pred_times=None, eval_times=None)


def test_split_invalid_y_type():
    cv = DummyCV(n_splits=2)
    X = pd.DataFrame({"a": [1, 2], "b": [3, 4]})
    pred_times = pd.Series([1, 2], index=X.index)
    eval_times = pd.Series([1, 2], index=X.index)
    with pytest.raises(ValueError, match="y should be a pandas Series"):
        cv.split(X, y=[1, 2], pred_times=pred_times, eval_times=eval_times)


def test_split_invalid_pred_times_type():
    cv = DummyCV(n_splits=2)
    X = pd.DataFrame({"a": [1, 2]})
    y = pd.Series([1, 2], index=X.index)
    eval_times = pd.Series([1, 2], index=X.index)
    with pytest.raises(ValueError, match="pred_times should be a pandas Series"):
        cv.split(X, y=y, pred_times=[1, 2], eval_times=eval_times)


def test_split_invalid_eval_times_type():
    cv = DummyCV(n_splits=2)
    X = pd.DataFrame({"a": [1, 2]})
    y = pd.Series([1, 2], index=X.index)
    pred_times = pd.Series([1, 2], index=X.index)
    with pytest.raises(ValueError, match="eval_times should be a pandas Series"):
        cv.split(X, y=y, pred_times=pred_times, eval_times=[1, 2])


def test_split_index_mismatch_y():
    cv = DummyCV(n_splits=2)
    X = pd.DataFrame({"a": [1, 2]}, index=[10, 11])
    y = pd.Series([1, 2], index=[99, 98])
    pred_times = pd.Series([1, 2], index=X.index)
    eval_times = pd.Series([1, 2], index=X.index)
    with pytest.raises(ValueError, match="X and y must have the same index"):
        cv.split(X, y=y, pred_times=pred_times, eval_times=eval_times)


def test_split_index_mismatch_pred_times():
    cv = DummyCV(n_splits=2)
    X = pd.DataFrame({"a": [1, 2]}, index=[1, 2])
    y = pd.Series([1, 2], index=[1, 2])
    pred_times = pd.Series([1, 2], index=[3, 4])
    eval_times = pd.Series([1, 2], index=[1, 2])
    with pytest.raises(ValueError, match="X and pred_times must have the same index"):
        cv.split(X, y=y, pred_times=pred_times, eval_times=eval_times)


def test_split_index_mismatch_eval_times():
    cv = DummyCV(n_splits=2)
    X = pd.DataFrame({"a": [1, 2]}, index=[1, 2])
    y = pd.Series([1, 2], index=[1, 2])
    pred_times = pd.Series([1, 2], index=[1, 2])
    eval_times = pd.Series([1, 2], index=[99, 98])
    with pytest.raises(ValueError, match="X and eval_times must have the same index"):
        cv.split(X, y=y, pred_times=pred_times, eval_times=eval_times)


def test_split_pred_times_not_sorted():
    cv = DummyCV(n_splits=2)
    X = pd.DataFrame({"a": [1, 2]}, index=[1, 2])
    y = pd.Series([1, 2], index=[1, 2])
    pred_times = pd.Series([2, 1], index=[1, 2])
    eval_times = pd.Series([1, 2], index=[1, 2])
    with pytest.raises(ValueError, match="pred_times should be sorted"):
        cv.split(X, y=y, pred_times=pred_times, eval_times=eval_times)


def test_split_eval_times_not_sorted():
    cv = DummyCV(n_splits=2)
    X = pd.DataFrame({"a": [1, 2]}, index=[1, 2])
    y = pd.Series([1, 2], index=[1, 2])
    pred_times = pd.Series([1, 2], index=[1, 2])
    eval_times = pd.Series([2, 1], index=[1, 2])
    with pytest.raises(ValueError, match="eval_times should be sorted"):
        cv.split(X, y=y, pred_times=pred_times, eval_times=eval_times)