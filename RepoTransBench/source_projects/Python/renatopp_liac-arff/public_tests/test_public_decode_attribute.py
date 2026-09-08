import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import arff

ARFF = '''@RELATION sample
@ATTRIBUTE "age in years" NUMERIC
@ATTRIBUTE gender {female,male}
@DATA
34,female
29,male
'''

class TestPublicDecodeAttribute(unittest.TestCase):
    def test_attribute_parsing(self):
        obj = arff.loads(ARFF)
        self.assertEqual(obj['attributes'][0][0], 'age in years')
        self.assertEqual(obj['attributes'][1][1], ('female', 'male'))
        self.assertEqual(obj['data'][1][1], 'male')