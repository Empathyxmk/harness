import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import arff

ARFF = '''%
% A dataset with comments
@RELATION xample

% List of attributes
@ATTRIBUTE val NUMERIC
@ATTRIBUTE state {t,f}

% List of observations
@DATA
1,t
2,f
% end comments
'''

class TestPublicDecodeComment(unittest.TestCase):
    def test_comments(self):
        obj = arff.loads(ARFF)
        self.assertEqual(obj['relation'], 'xample')
        self.assertEqual(obj['data'], [[1, 't'], [2, 'f']])