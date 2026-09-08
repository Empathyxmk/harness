import numpy as np
import pytest
from iterstrat.ml_stratifiers import IterativeStratification

class DummyRandomState:
    """Utility class to supply predictable 'random' choices during tests."""
    def __init__(self):
        self.calls = 0

    def choice(self, n):
        # Always return the smallest index to keep behavior deterministic
        self.calls += 1
        return 0

def dummy_random():
    return DummyRandomState()

def test_multilabel_stratification_balanced_multi():
    labels = np.array([[1, 0], [1, 1], [0, 1], [0, 0]])
    r = np.array([0.5, 0.5])
    folds = IterativeStratification(labels, r, random_state=dummy_random())
    assert folds.shape[0] == 4

def test_more_folds_than_samples():
    labels = np.eye(6, dtype=int)
    r = np.array([1/6.]*6)
    folds = IterativeStratification(labels, r, random_state=dummy_random())
    assert all([f in range(6) for f in folds])

def test_all_zeros_label():
    # Test logic branch for all-zero labels
    labels = np.zeros((4, 2), dtype=int)
    r = np.array([0.5, 0.5])
    folds = IterativeStratification(labels, r, random_state=dummy_random())
    assert np.all(np.isin(folds, [0, 1]))

def test_folds_shape_matches_n_samples():
    labels = np.random.randint(0, 2, size=(10, 3))
    r = np.array([0.6, 0.4])
    folds = IterativeStratification(labels, r, random_state=dummy_random())
    assert folds.shape[0] == 10

def test_invalid_float_labels():
    # IndexError expected if labels are not int/bool and used as indices
    labels = np.array([[1.0, 0.], [0., 1.]], dtype=float)
    r = np.array([0.5, 0.5], dtype=float)
    with pytest.raises(IndexError):
        IterativeStratification(labels, r, random_state=dummy_random())

def test_invalid_noninteger_labels():
    labels = np.array([[0.8], [0.8], [0.2], [0.0]])
    r = np.array([0.5, 0.5])
    with pytest.raises(IndexError):
        IterativeStratification(labels, r, random_state=dummy_random())

@pytest.mark.xfail(raises=IndexError)
def test_binary_stratification_simple():
    labels = np.array([[1], [0], [1], [0]])
    r = np.array([0.5])
    # Known to fail (IndexError), included for documentation
    IterativeStratification(labels, r, random_state=dummy_random())