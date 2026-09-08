import numpy as np
import os
import tempfile
from py_ir1d_darkface_eval_tools.read_pred import read_pred

import pytest

class DummyTestCase:
    """Minimal substitute for Matlab TestCase."""
    def assertEqual(self, a, b):
        np.testing.assert_allclose(a, b)

    def verifyTrue(self, cond):
        assert cond

    def assertContains(self, s, substring, msg=None):
        assert substring in s, msg

def make_pred_file(directory, filename, lines):
    fpath = os.path.join(directory, filename)
    with open(fpath,'w') as f:
        for line in lines:
            f.write(" ".join(str(x) for x in line)+'\n')
    return fpath

def make_file_list(directory, files):
    return [[os.path.join(directory, f) for f in files]]

def test_valid_prediction_file():
    with tempfile.TemporaryDirectory() as td:
        valid_lines = [
            [10,10,20,20,0.95],
            [30,30,40,40,0.80],
            [15,15,25,25,0.99]
        ]
        valid_file = make_pred_file(td, "valid_pred.txt", valid_lines)
        empty_file = make_pred_file(td, "empty_pred.txt", [])
        invalid_file = os.path.join(td, "invalid_pred.txt")
        with open(invalid_file, "w") as f:
            f.write("10 10 20 20 0.95\n")
            f.write("invalid line content\n")
            f.write("15 15 25 25 0.99\n")
        files = ['valid_pred.txt', 'non_existent_pred.txt', 'empty_pred.txt', 'invalid_pred.txt']
        file_list = make_file_list(td, files)
        sub_folder = td
        pred_list = read_pred("", file_list, sub_folder)
        actual_pred = pred_list[0][0]
        expected_pred = np.array([
            [15,15,25,25,0.99],
            [10,10,20,20,0.95],
            [30,30,40,40,0.80]
        ])
        np.testing.assert_allclose(actual_pred, expected_pred, atol=1e-6)

def test_non_existent_prediction_file():
    with tempfile.TemporaryDirectory() as td:
        valid_file = make_pred_file(td, "valid_pred.txt", [[10,10,20,20,0.95]])
        file_list = make_file_list(td, ['valid_pred.txt', 'non_existent_pred.txt'])
        sub_folder = td
        pred_list = read_pred("", file_list, sub_folder)
        assert pred_list[0][1] == []

def test_empty_prediction_file():
    with tempfile.TemporaryDirectory() as td:
        empty_file = make_pred_file(td, "empty_pred.txt", [])
        file_list = make_file_list(td, ['empty_pred.txt'])
        sub_folder = td
        pred_list = read_pred("", file_list, sub_folder)
        pred = pred_list[0][0]
        assert pred == [] or (hasattr(pred, 'size') and pred.size == 0)

def test_invalid_prediction_file_format():
    with tempfile.TemporaryDirectory() as td:
        invalid_file = os.path.join(td, "invalid_pred.txt")
        with open(invalid_file, "w") as f:
            f.write("10 10 20 20 0.95\n")
            f.write("invalid line content\n")
            f.write("15 15 25 25 0.99\n")
        file_list = make_file_list(td, ["invalid_pred.txt"])
        sub_folder = td
        pred_list = read_pred("", file_list, sub_folder)
        assert pred_list[0][0] == []