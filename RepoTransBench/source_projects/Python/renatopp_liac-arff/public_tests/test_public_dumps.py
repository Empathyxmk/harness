import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import arff

OBJ = {
    'description': 'public dataset',
    'relation': 'public_example',
    'attributes': [
        ('title', 'STRING'),
        ('amount', 'NUMERIC'),
        ('flag', ('Y', 'N'))
    ],
    'data': [
        ['alpha', 50, 'Y'],
        ['beta', 100.1, 'N']
    ]
}

EXPECTED = '''% public dataset
@RELATION public_example

@ATTRIBUTE title STRING
@ATTRIBUTE amount NUMERIC
@ATTRIBUTE flag {Y, N}

@DATA
alpha,50,Y
beta,100.1,N
'''

class TestPublicDumps(unittest.TestCase):
    def test_dumps(self):
        s = arff.dumps(OBJ)
        self.assertEqual(s, EXPECTED)
        loaded = arff.loads(s)
        self.assertEqual(loaded['description'], 'public dataset')
        self.assertEqual(loaded['relation'], 'public_example')
        self.assertEqual(loaded['data'], OBJ['data'])