import numpy as np
import pytest
from iterstrat.ml_stratifiers import IterativeStratification

class DummyRandomState:
    """Utility class to supply predictable 'random' choices during tests."""
    def __init__(self):
        self.calls = 0

    def choice(self, n):
        # Always return the largest index for alternative deterministic behavior
        self.calls += 1
        return n - 1

def dummy_random():
    return DummyRandomState()

def test_multilabel_stratification_balanced_multi_public():
    labels = np.array([[0, 1], [1, 0], [1, 1], [0, 0]])
    r = np.array([0.7, 0.3])
    folds = IterativeStratification(labels, r, random_state=dummy_random())
    assert folds.shape[0] == 4

def test_more_folds_than_samples_public():
    labels = np.flipud(np.eye(5, dtype=int))
    r = np.array([1/5.]*5)
    folds = IterativeStratification(labels, r, random_state=dummy_random())
    assert all([f in range(5) for f in folds])

def test_all_zeros_label_public():
    labels = np.zeros((3, 4), dtype=int)
    r = np.array([0.34, 0.33, 0.33])
    folds = IterativeStratification(labels, r, random_state=dummy_random())
    assert np.all(np.isin(folds, [0, 1, 2]))

def test_folds_shape_matches_n_samples_public():
    labels = np.random.randint(0, 2, size=(7, 4))
    r = np.array([0.3, 0.7])
    folds = IterativeStratification(labels, r, random_state=dummy_random())
    assert folds.shape[0] == 7

def test_invalid_float_labels_public():
    labels = np.array([[0.2, 1.0], [1.0, 0.2]], dtype=float)
    r = np.array([0.6, 0.4], dtype=float)
    with pytest.raises(IndexError):
        IterativeStratification(labels, r, random_state=dummy_random())

def test_invalid_noninteger_labels_public():
    labels = np.array([[0.5], [0.5], [0.5], [0.0]])
    r = np.array([0.9, 0.1])
    with pytest.raises(IndexError):
        IterativeStratification(labels, r, random_state=dummy_random())

@pytest.mark.xfail(raises=IndexError)
def test_binary_stratification_simple_public():
    labels = np.array([[0], [1], [0], [1]])
    r = np.array([0.5])
    IterativeStratification(labels, r, random_state=dummy_random())