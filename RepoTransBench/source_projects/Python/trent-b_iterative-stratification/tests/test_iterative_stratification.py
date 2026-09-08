import numpy as np
import pytest
from iterstrat.ml_stratifiers import IterativeStratification

class DummyRandomState:
    def __init__(self):
        self.calls = 0
    def choice(self, n):
        # Always select the first for deterministic output
        self.calls += 1
        return 0

@pytest.mark.parametrize(
    "labels, r, expected_num_folds",
    [
        (np.array([[1,0,1],[1,1,0],[0,1,1],[1,0,0],[0,0,0]]), np.array([0.6,0.4]), 2),
        pytest.param(np.array([[1],[1],[1],[0]]), np.array([0.5, 0.5]), 2, marks=pytest.mark.xfail(raises=IndexError)),
    ]
)
def test_iterative_stratification_varied(labels, r, expected_num_folds):
    rs = DummyRandomState()
    out = IterativeStratification(labels, r, rs)
    assert out.shape[0] == labels.shape[0]
    assert np.all(np.isin(out, np.arange(expected_num_folds)))

def test_iterative_stratification_all_ones_label():
    labels = np.ones((5, 2), dtype=int)
    r = np.array([0.4, 0.6])
    out = IterativeStratification(labels, r, DummyRandomState())
    assert out.shape == (5,)

def test_iterative_stratification_single_fold():
    labels = np.eye(4, dtype=int)
    r = np.array([1.0])
    out = IterativeStratification(labels, r, DummyRandomState())
    assert np.all(out == 0)

def test_iterative_stratification_random_output_types():
    labels = np.array([[1, 0], [1, 1]])
    r = np.array([0.5, 0.5])
    rs = DummyRandomState()
    out = IterativeStratification(labels, r, rs)
    assert out.dtype == np.int_

def test_iterative_stratification_all_zero_labels_branch():
    # Branch where only all-zero labels are left
    labels = np.zeros((4, 2), dtype=int)
    r = np.array([0.25, 0.25, 0.25, 0.25])
    out = IterativeStratification(labels, r, DummyRandomState())
    assert out.shape[0] == 4
    assert np.all(np.isin(out, range(4)))