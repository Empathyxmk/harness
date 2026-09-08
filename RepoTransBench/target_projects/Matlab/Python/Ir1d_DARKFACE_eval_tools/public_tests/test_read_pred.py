import numpy as np
import os
import tempfile
from py_ir1d_darkface_eval_tools.read_pred import read_pred

def test_read_simple_pred():
    data = np.array([
        [10, 20, 15, 25, 0.50],
        [25, 25, 10, 10, 0.80]
    ])
    with tempfile.TemporaryDirectory() as td:
        fname = os.path.join(td, 'public_test_pred_simple.txt')
        # Write space-separated, 5 columns
        np.savetxt(fname, data, fmt="%.2f")
        # Simulate 'pwd' and file_list
        file_list = [[fname]]
        sub_folder = td
        # Since our translation expects file_list entries like './data/gt/...' to replace, simulate accordingly
        # But use as is for simplicity here
        pred_list = read_pred("", file_list, "")
        pred = pred_list[0][0]
        # Should be sorted by score descending, so row 1 should come before row 0
        sorted_data = data[np.argsort(-data[:,4])]
        np.testing.assert_allclose(pred, sorted_data, atol=1e-12)

def test_read_empty_pred():
    data = np.zeros((0, 5))
    with tempfile.TemporaryDirectory() as td:
        fname = os.path.join(td, 'public_test_pred_empty.txt')
        # Write empty file
        with open(fname, 'w') as f:
            pass
        file_list = [[fname]]
        pred_list = read_pred("", file_list, "")
        pred = pred_list[0][0]
        assert pred == [] or (hasattr(pred, 'size') and pred.size == 0)