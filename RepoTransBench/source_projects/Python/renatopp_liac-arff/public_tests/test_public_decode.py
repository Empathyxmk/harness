import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import arff

SIMPLE_ARFF = '''
% Simple dataset
@RELATION public_relation

@ATTRIBUTE feature1 NUMERIC
@ATTRIBUTE feature2 {low,medium,high}

@DATA
1.2,low
3.4,medium
5.6,high
'''

class TestPublicDecode(unittest.TestCase):
    def test_decode(self):
        obj = arff.decode(SIMPLE_ARFF.splitlines())
        self.assertEqual(obj['relation'], 'public_relation')
        self.assertEqual(len(obj['attributes']), 2)
        self.assertEqual(obj['attributes'][0][0], 'feature1')
        self.assertEqual(obj['attributes'][1][1], ('low', 'medium', 'high'))
        self.assertEqual(obj['data'], [[1.2, 'low'], [3.4, 'medium'], [5.6, 'high']])