import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import arff

OBJ = {
    'description': 'public encode test',
    'relation': 'encode_case2',
    'attributes': [
        ('val', 'NUMERIC'),
        ('label', ('good','bad'))
    ],
    'data': [
        [10, 'good'],
        [20, 'bad']
    ]
}

class TestPublicEncode(unittest.TestCase):
    def test_encode_func(self):
        s = arff.dumps(OBJ)
        self.assertIn('public encode test', s)
        obj2 = arff.loads(s)
        self.assertEqual(obj2['relation'], 'encode_case2')
        self.assertEqual(obj2['data'][1][0], 20)