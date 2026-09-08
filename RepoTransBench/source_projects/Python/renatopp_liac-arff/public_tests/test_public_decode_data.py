import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import arff

ARFF = '''@RELATION grades

@ATTRIBUTE mark NUMERIC
@ATTRIBUTE passfail {pass,fail}

@DATA
95,pass
67,fail
'''

class TestPublicDecodeData(unittest.TestCase):
    def test_decode_data(self):
        obj = arff.loads(ARFF)
        self.assertEqual(obj['data'], [[95, 'pass'], [67, 'fail']])