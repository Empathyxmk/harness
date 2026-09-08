import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import arff

ARFF = '''@RELATION foo

@ATTRIBUTE a NUMERIC
@ATTRIBUTE b {p,q}

@DATA
14,p
20,q
'''

class TestPublicLoadsDumps(unittest.TestCase):
    def test_loads_dumps_roundtrip(self):
        aobj = arff.loads(ARFF)
        s = arff.dumps(aobj)
        obj2 = arff.loads(s)
        self.assertEqual(aobj['relation'], obj2['relation'])
        self.assertEqual(aobj['data'], obj2['data'])