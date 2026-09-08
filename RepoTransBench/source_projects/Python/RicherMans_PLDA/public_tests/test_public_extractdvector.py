import os
import tempfile
import numpy as np
import sys
import unittest

# Import the extractdvector module robustly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../scoring')))
import extractdvector

class TestPublicExtractDVector(unittest.TestCase):
    def test_dummy_extract_public(self):
        X = np.array([[5,7],[9,11]])
        v = extractdvector.dummy_extract_dvector(X)
        np.testing.assert_allclose(v, [7,9])

    def test_main_usage_public(self):
        # check exit code if not enough args (same logic, public name)
        ret = extractdvector.main(["extractdvector.py"])
        self.assertEqual(ret, 1)

    def test_main_ok_public(self):
        # Test file output with output file created and checked array
        with tempfile.TemporaryDirectory() as tmpdir:
            out_path = os.path.join(tmpdir, "public_out.pkl")
            # The code always returns [2, 3] (see extractdvector.py), so test that value
            ret = extractdvector.main(["extractdvector.py", "dummy_in", out_path])
            self.assertEqual(ret, 0)
            import pickle
            with open(out_path, "rb") as f:
                arr = pickle.load(f)
            np.testing.assert_allclose(arr, [2,3])

if __name__ == '__main__':
    unittest.main()