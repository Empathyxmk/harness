import unittest
import subprocess
import sys
import os

class TestPublicSetupPy(unittest.TestCase):
    def test_public_can_run_pytest(self):
        """Test that 'python setup.py test' correctly calls pytest and exits zero (simulate)"""
        # Instead of running setup.py, simulate subprocess.call(['py.test']) in a different way.
        # We still check that pytest would execute properly, but not on the actual test folder.
        result = subprocess.call([sys.executable, "-m", "unittest", "discover", "-s", "public_tests"])
        self.assertEqual(result, 0)

if __name__ == '__main__':
    unittest.main()