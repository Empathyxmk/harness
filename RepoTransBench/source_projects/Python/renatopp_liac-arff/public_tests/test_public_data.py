import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import arff

ARFF = '''@RELATION car_eval

@ATTRIBUTE buying {cheap,expensive}
@ATTRIBUTE safety {high,low}
@ATTRIBUTE class {good,bad}

@DATA
cheap,high,good
expensive,low,bad
'''

class TestPublicData(unittest.TestCase):
    def test_data_parse(self):
        obj = arff.loads(ARFF)
        self.assertEqual(obj['attributes'][0][1], ('cheap', 'expensive'))
        self.assertEqual(obj['attributes'][1][1], ('high', 'low'))
        self.assertEqual(obj['attributes'][2][1], ('good', 'bad'))
        self.assertEqual(obj['data'][0][0], 'cheap')
        self.assertEqual(obj['data'][1][2], 'bad')