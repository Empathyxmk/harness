import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import arff

OBJ = {
    'description': 'Encode attribute sample',
    'relation': 'encode_sample',
    'attributes': [
        ('item', 'STRING'),
        ('amt', 'NUMERIC'),
        ('col', ('A','B','C'))
    ],
    'data': [
        ["item1", 123, 'A'],
        ["item2", 80.7, 'B'],
        ["item3", 61, 'C']
    ]
}

class TestPublicEncodeAttribute(unittest.TestCase):
    def test_attribute_encoding(self):
        s = arff.dumps(OBJ)
        self.assertIn('@ATTRIBUTE item STRING', s)
        self.assertIn('@ATTRIBUTE amt NUMERIC', s)
        self.assertIn('@ATTRIBUTE col {A, B, C}', s)
        obj = arff.loads(s)
        self.assertEqual(obj['data'][1][2], 'B')