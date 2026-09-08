import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import arff

OBJ = {
    'description': 'convert',
    'relation': 'convert_case',
    'attributes': [
        ('temperature', 'REAL'),
        ('weather', ('sunny','rainy')),
    ],
    'data': [
        [23.5, 'sunny'],
        [16.2, 'rainy']
    ]
}

class TestPublicConversor(unittest.TestCase):
    def test_to_from_string(self):
        s = arff.dumps(OBJ)
        out = arff.loads(s)
        self.assertEqual(out['data'], OBJ['data'])
        self.assertEqual(out['relation'], 'convert_case')