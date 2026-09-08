import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import arff

OBJ = {
    'description': 'This is a public comment',
    'relation': 'comments_case',
    'attributes': [
        ('id', 'NUMERIC'),
        ('label', ('A','B'))
    ],
    'data': [
        [1,'A'],
        [2,'B']
    ]
}

class TestPublicEncodeComment(unittest.TestCase):
    def test_encode_comment(self):
        s = arff.dumps(OBJ)
        self.assertTrue('This is a public comment' in s)
        self.assertIn('@RELATION comments_case', s)
        self.assertIn('@ATTRIBUTE id NUMERIC', s)
        self.assertIn('@ATTRIBUTE label {A, B}', s)