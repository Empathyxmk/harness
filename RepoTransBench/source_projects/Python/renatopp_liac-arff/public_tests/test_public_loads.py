import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import arff

ARFF = '''@RELATION public_sample

@ATTRIBUTE id NUMERIC
@ATTRIBUTE class {p, q}

@DATA
101,p
102,q
'''

class TestPublicLoads(unittest.TestCase):
    def test_loads(self):
        obj = arff.loads(ARFF)
        self.assertEqual(obj['relation'], 'public_sample')
        self.assertEqual(obj['attributes'][1][1], ('p', 'q'))
        self.assertEqual(obj['data'][0][1], 'p')
        self.assertEqual(obj['data'][1][0], 102)