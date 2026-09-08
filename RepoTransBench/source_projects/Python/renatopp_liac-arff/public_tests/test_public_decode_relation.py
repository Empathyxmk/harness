import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import arff

ARFF = '''@relation myrel
@attribute a numeric
@attribute b {yes,no}
@data
1,yes
2,no
'''

class TestPublicDecodeRelation(unittest.TestCase):
    def test_relation_parsing(self):
        obj = arff.loads(ARFF)
        self.assertEqual(obj['relation'], 'myrel')
        self.assertEqual(obj['attributes'][1][1], ('yes','no'))
        self.assertEqual(obj['data'][1][1], 'no')