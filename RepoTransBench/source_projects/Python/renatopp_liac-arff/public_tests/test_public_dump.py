import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import arff

OBJ = {
    'description': 'For dump test',
    'relation': 'my_dump_test',
    'attributes': [
        ('foo', 'NUMERIC'),
        ('bar', ('ON','OFF'))
    ],
    'data': [
        [111, 'ON'],
        [99, 'OFF']
    ]
}

class TestPublicDump(unittest.TestCase):
    def test_dump(self):
        s = arff.dumps(OBJ)
        obj2 = arff.loads(s)
        self.assertEqual(obj2['relation'], OBJ['relation'])
        self.assertEqual(obj2['data'][0][0], 111)