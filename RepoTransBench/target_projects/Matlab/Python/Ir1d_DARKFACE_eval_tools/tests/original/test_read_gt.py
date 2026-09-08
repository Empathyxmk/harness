import numpy as np
import os
import tempfile
from py_ir1d_darkface_eval_tools.read_gt import read_gt

import pytest

class DummyTestCase:
    """Minimal dummy class to substitute Matlab TestCase for assert checks."""
    def assertEqual(self, a, b):
        np.testing.assert_array_equal(a, b)

    def verifyTrue(self, cond):
        assert cond

    def assertContains(self, s, substring, msg=None):
        assert substring in s, msg

def make_gt_file(directory, filename, content):
    fpath = os.path.join(directory, filename)
    with open(fpath,'w') as f:
        f.write(content)
    return fpath

def make_file_list(directory, files):
    return [[os.path.join(directory, f) for f in files]]

def test_valid_gt_file():
    with tempfile.TemporaryDirectory() as td:
        # GT: "2\n" "10 10 20 20\n" "30 30 40 40\n"
        valid_file = make_gt_file(td, "valid_gt.txt", "2\n10 10 20 20\n30 30 40 40\n")
        files = ['valid_gt.txt', 'non_existent_gt.txt', 'empty_gt.txt', 'invalid_gt.txt']
        # empty_gt.txt
        empty_file = make_gt_file(td, "empty_gt.txt", "0\n")
        # invalid_gt.txt
        inv_file = make_gt_file(td, "invalid_gt.txt", "abc\n10 10 20 20\n")
        file_list = make_file_list(td, files)
        gt_folder = td
        gt_list = read_gt("", file_list, gt_folder)
        actual_gt = gt_list[0][0]
        expected_gt = np.array([[10,10,20,20],[30,30,40,40]])
        np.testing.assert_array_equal(actual_gt, expected_gt)

def test_non_existent_gt_file():
    # Makes sure 'break' disables further files in that event
    with tempfile.TemporaryDirectory() as td:
        valid_file = make_gt_file(td, "valid_gt.txt", "2\n10 10 20 20\n30 30 40 40\n")
        file_list = make_file_list(td, ['valid_gt.txt', 'non_existent_gt.txt', 'empty_gt.txt', 'invalid_gt.txt'])
        gt_folder = td
        gt_list = read_gt("", file_list, gt_folder)
        # Index 1 is for non_existent_gt.txt and should be empty
        assert gt_list[0][1] == []
        assert gt_list[0][2] == []
        assert gt_list[0][3] == []

def test_empty_gt_file():
    with tempfile.TemporaryDirectory() as td:
        empty_file = make_gt_file(td, "empty_gt.txt", "0\n")
        file_list = make_file_list(td, ['empty_gt.txt'])
        gt_folder = td
        gt_list = read_gt("", file_list, gt_folder)
        assert gt_list[0][0] == [] or (hasattr(gt_list[0][0], 'size') and gt_list[0][0].size == 0)

def test_invalid_gt_file_format():
    with tempfile.TemporaryDirectory() as td:
        inv_file = make_gt_file(td, "invalid_gt.txt", "abc\n10 10 20 20\n")
        file_list = make_file_list(td, ['invalid_gt.txt'])
        gt_folder = td
        gt_list = read_gt("", file_list, gt_folder)
        # Due to exception, should be empty
        assert gt_list[0][0] == []