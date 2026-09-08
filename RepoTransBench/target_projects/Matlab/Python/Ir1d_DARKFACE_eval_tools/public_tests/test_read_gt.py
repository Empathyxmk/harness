import numpy as np
import os
import tempfile
from py_ir1d_darkface_eval_tools.read_gt import read_gt

def test_read_simple_gt():
    gt_data = np.array([
        [1, 2, 30, 40],
        [7, 8, 20, 10]
    ])
    with tempfile.TemporaryDirectory() as td:
        fname = os.path.join(td, 'public_test_gt_simple.txt')
        # Write first line = 2, then two rows
        with open(fname, 'w') as f:
            f.write("2\n")
            for row in gt_data:
                f.write(" ".join(str(int(x)) for x in row) + "\n")
        file_list = [[fname]]
        gt_list = read_gt("", file_list, "")
        gt = gt_list[0][0]
        np.testing.assert_array_equal(gt, gt_data)

def test_read_empty_gt():
    with tempfile.TemporaryDirectory() as td:
        fname = os.path.join(td, 'public_test_gt_empty.txt')
        with open(fname, 'w') as f:
            f.write("0\n")
        file_list = [[fname]]
        gt_list = read_gt("", file_list, "")
        gt = gt_list[0][0]
        assert gt == [] or (hasattr(gt, 'size') and gt.size == 0)