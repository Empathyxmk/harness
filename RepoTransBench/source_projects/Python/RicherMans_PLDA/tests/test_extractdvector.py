import os
import tempfile
import numpy as np
import builtins
import sys
import importlib.util
import types

import unittest

# Import the extractdvector module robustly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../scoring')))
import extractdvector

class TestExtractDVector(unittest.TestCase):
    def test_dummy_extract(self):
        X = np.array([[1,2],[3,4]])
        v = extractdvector.dummy_extract_dvector(X)
        np.testing.assert_allclose(v, [2,3])

    def test_main_usage(self):
        # check exit code if not enough args
        ret = extractdvector.main(["extractdvector.py"])
        self.assertEqual(ret, 1)

    def test_main_ok(self):
        # Test file output
        with tempfile.TemporaryDirectory() as tmpdir:
            out_path = os.path.join(tmpdir, "out.pkl")
            ret = extractdvector.main(["extractdvector.py", "dummy_in", out_path])
            self.assertEqual(ret, 0)
            import pickle
            with open(out_path, "rb") as f:
                arr = pickle.load(f)
            np.testing.assert_allclose(arr, [2,3])

if __name__ == '__main__':
    unittest.main()