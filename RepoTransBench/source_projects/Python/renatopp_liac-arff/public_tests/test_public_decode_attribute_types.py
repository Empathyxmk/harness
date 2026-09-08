import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import arff

ARFF = """
@RELATION testr

@ATTRIBUTE first NUMERIC
@ATTRIBUTE second INTEGER
@ATTRIBUTE third REAL
@ATTRIBUTE some {'a','b'}
@ATTRIBUTE fifth STRING

@DATA
9,5,3.14,'a',"text1"
10,20,2.72,'b',"text2"
"""

class TestPublicDecodeAttributeTypes(unittest.TestCase):
    def test_types(self):
        obj = arff.loads(ARFF)
        attrs = obj['attributes']
        self.assertEqual([a[1] for a in attrs[:3]], ['NUMERIC', 'INTEGER', 'REAL'])
        self.assertEqual(attrs[3][1], ('a','b'))
        self.assertEqual(attrs[4][1], 'STRING')
        self.assertEqual(obj['data'][0][0], 9)
        self.assertEqual(obj['data'][1][3], 'b')