import unittest
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import arff

ARFF_FILE = os.path.join(os.path.dirname(__file__), 'test_public_load_file.arff')

ARFF_CONTENT = '''% small test file
@RELATION user_data
@ATTRIBUTE uid NUMERIC
@ATTRIBUTE uname STRING
@DATA
77,alice
88,bob
'''

class TestPublicLoad(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open(ARFF_FILE, 'w') as f:
            f.write(ARFF_CONTENT)

    @classmethod
    def tearDownClass(cls):
        os.remove(ARFF_FILE)

    def test_file_loading(self):
        with open(ARFF_FILE, 'r') as fp:
            obj = arff.load(fp)
            self.assertEqual(obj['relation'], 'user_data')
            self.assertEqual(obj['data'][0][1], 'alice')
            self.assertEqual(obj['data'][1][0], 88)