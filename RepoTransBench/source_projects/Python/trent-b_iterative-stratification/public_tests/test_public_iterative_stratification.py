import numpy as np
import pytest
from iterstrat.ml_stratifiers import IterativeStratification

class DummyRandomState:
    def __init__(self):
        self.calls = 0
    def choice(self, n):
        # Always select the last for alternative deterministic output
        self.calls += 1
        return n - 1

@pytest.mark.parametrize(
    "labels, r, expected_num_folds",
    [
        (np.array([[0,1,0],[0,0,1],[1,1,0],[0,1,1],[1,0,1]]), np.array([0.7,0.3]), 2),
        pytest.param(np.array([[0],[0],[1],[1]]), np.array([0.4, 0.6]), 2, marks=pytest.mark.xfail(raises=IndexError)),
    ]
)
def test_iterative_stratification_varied_public(labels, r, expected_num_folds):
    rs = DummyRandomState()
    out = IterativeStratification(labels, r, rs)
    assert out.shape[0] == labels.shape[0]
    assert np.all(np.isin(out, np.arange(expected_num_folds)))

def test_iterative_stratification_all_ones_label_public():
    labels = np.ones((4, 3), dtype=int)
    r = np.array([0.2, 0.4, 0.4])
    out = IterativeStratification(labels, r, DummyRandomState())
    assert out.shape == (4,)

def test_iterative_stratification_single_fold_public():
    labels = np.eye(5, dtype=int)
    r = np.array([1.0])
    out = IterativeStratification(labels, r, DummyRandomState())
    assert np.all(out == 0)

def test_iterative_stratification_random_output_types_public():
    labels = np.array([[0, 1], [1, 1]])
    r = np.array([0.7, 0.3])
    rs = DummyRandomState()
    out = IterativeStratification(labels, r, rs)
    assert out.dtype == np.int_

def test_iterative_stratification_all_zero_labels_branch_public():
    labels = np.zeros((3, 5), dtype=int)
    r = np.array([0.2, 0.2, 0.2, 0.2, 0.2])
    out = IterativeStratification(labels, r, DummyRandomState())
    assert out.shape[0] == 3
    assert np.all(np.isin(out, range(5)))