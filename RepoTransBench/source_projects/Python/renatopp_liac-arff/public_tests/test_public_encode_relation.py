import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import arff

OBJ = {
    'description': 'Encode relation public',
    'relation': 'public_relation',
    'attributes': [
        ('k', 'NUMERIC'),
        ('v', ('X','Y'))
    ],
    'data': [
        [3, 'X'],
        [4, 'Y']
    ]
}

class TestPublicEncodeRelation(unittest.TestCase):
    def test_encode_relation(self):
        s = arff.dumps(OBJ)
        self.assertIn('Encode relation public', s)
        self.assertIn('@RELATION public_relation', s)
        self.assertIn('@ATTRIBUTE k NUMERIC', s)
        obj = arff.loads(s)
        self.assertEqual(obj['data'][1][1], 'Y')