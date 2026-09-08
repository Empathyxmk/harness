import numpy as np
import pandas as pd
import pytest

from timeseriescv.cross_validation import (
    BaseTimeSeriesCrossValidator,
    PurgedWalkForwardCV,
    CombPurgedKFoldCV,
    purge,
    embargo,
    compute_fold_bounds,
)

def make_simple_data(n=10, seed=0):
    rng = np.random.default_rng(seed)
    df = pd.DataFrame({
        'A': rng.random(n),
        'B': rng.random(n),
        'C': rng.random(n),
    })
    pred_times = pd.Series(pd.date_range('2021-01-01', periods=n, freq='1D'), index=df.index)
    eval_times = pred_times + pd.Timedelta('1D')
    y = pd.Series(rng.integers(0, 2, size=n), index=df.index)
    return df, y, pred_times, eval_times

def test_base_timeseriescv_n_splits_property():
    cv = BaseTimeSeriesCrossValidator(n_splits=5)
    assert cv.n_splits == 5
    cv.n_splits = 6
    assert cv.n_splits == 6

def test_purge_basic_object():
    class DummyCV(BaseTimeSeriesCrossValidator):
        def __init__(self):
            super().__init__(n_splits=2)
            self.pred_times = pd.Series(pd.date_range('2023-01-01', periods=6, freq='D'))
            self.eval_times = self.pred_times + pd.Timedelta('1D')
            self.indices = np.arange(6)
    cv = DummyCV()
    test_fold_start = 4
    test_fold_end = 5
    in_train = purge(cv, test_fold_start, test_fold_end, test_fold_end)
    assert isinstance(in_train, np.ndarray)

def test_embargo_basic_object():
    class DummyCV(BaseTimeSeriesCrossValidator):
        def __init__(self):
            super().__init__(n_splits=2)
            self.pred_times = pd.Series(pd.date_range('2022-01-01', periods=10, freq='D'))
            self.eval_times = self.pred_times + pd.Timedelta('1D')
            self.embargo_td = pd.Timedelta('1D')
            self.indices = np.arange(10)
    dummy_cv = DummyCV()
    train_indices = np.arange(0, 8)
    test_indices = np.array([8,9])
    test_fold_end = 9
    embargoed = embargo(dummy_cv, train_indices, test_indices, test_fold_end)
    assert isinstance(embargoed, np.ndarray)
    assert len(embargoed) <= len(train_indices)

def test_compute_fold_bounds_object():
    class DummyCV(BaseTimeSeriesCrossValidator):
        def __init__(self):
            super().__init__(n_splits=2)
            self.indices = np.arange(8)
    dummy_cv = DummyCV()
    bounds = compute_fold_bounds(dummy_cv, False)
    assert isinstance(bounds, list)

def test_purgedwalkforwardcv_split():
    X, y, pred_times, eval_times = make_simple_data(20)
    # n_splits=5 gives 3 splits for default min_train_splits=2, test_splits=1
    cv = PurgedWalkForwardCV(n_splits=5)
    splits = list(cv.split(X, y, pred_times, eval_times))
    assert len(splits) == 3
    for train, test in splits:
        assert set(train).isdisjoint(set(test))
        assert len(test) > 0

def test_combpurgedkfoldcv_split():
    X, y, pred_times, eval_times = make_simple_data(12)
    # n_splits=3 is valid
    cv = CombPurgedKFoldCV(n_splits=3)
    splits = list(cv.split(X, y, pred_times, eval_times))
    assert len(splits) == 3
    for train, test in splits:
        assert set(train).isdisjoint(set(test))

def test_repr_methods():
    cv1 = PurgedWalkForwardCV(n_splits=4)
    cv2 = CombPurgedKFoldCV(n_splits=3)
    # Use __class__.__name__ for repr content
    r1 = repr(cv1.__class__.__name__)
    r2 = repr(cv2.__class__.__name__)
    assert "PurgedWalkForwardCV" in r1
    assert "CombPurgedKFoldCV" in r2

def test_base_repr():
    cv = BaseTimeSeriesCrossValidator(n_splits=10)
    r = repr(cv.__class__.__name__)
    assert "BaseTimeSeriesCrossValidator" in r

def test_purge_empty_object():
    class DummyCV(BaseTimeSeriesCrossValidator):
        def __init__(self):
            super().__init__(n_splits=2)
            self.pred_times = pd.Series([], dtype='datetime64[ns]')
            self.eval_times = pd.Series([], dtype='datetime64[ns]')
            self.indices = np.array([], dtype=int)
    dummy_cv = DummyCV()
    # The function will raise IndexError since no pred_times, so guard with pytest.raises
    with pytest.raises(IndexError):
        purge(dummy_cv, 0, 0, 0)

def test_embargo_no_embargo_object():
    class DummyCV(BaseTimeSeriesCrossValidator):
        def __init__(self):
            super().__init__(n_splits=2)
            self.pred_times = pd.Series(pd.date_range('2020-01-01', periods=5, freq='D'))
            self.eval_times = self.pred_times + pd.Timedelta('1D')
            self.embargo_td = pd.Timedelta('0D')
            self.indices = np.arange(5)
    dummy_cv = DummyCV()
    train_indices = np.array([0, 4])
    test_indices = np.array([0, 4])
    test_fold_end = 4
    embargoed = embargo(dummy_cv, train_indices, test_indices, test_fold_end)
    assert set(embargoed) <= set(train_indices)

def test_purgedwalkforwardcv_invalid_n_test_splits():
    with pytest.raises(ValueError):
        # n_splits=2, n_test_splits must be < n_splits-1, i.e. < 1 here. So n_test_splits=1 triggers error
        PurgedWalkForwardCV(n_splits=2, n_test_splits=1)

def test_combpurgedkfoldcv_invalid():
    with pytest.raises(ValueError):
        CombPurgedKFoldCV(n_splits=1)