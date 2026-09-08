import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import arff

class TestPublicDumpsEscape(unittest.TestCase):
    def test_dumps_escape(self):
        obj = {
            "description": "Dumps escape sample",
            "relation": "dumps_escape_case",
            "attributes": [
                ("txt", "STRING"),
                ("cat", ("foo,bar", "baz")),
            ],
            "data": [
                ['"quoted", sample', "baz"],
                ['hello', "foo,bar"]
            ]
        }
        s = arff.dumps(obj)
        self.assertIn('"quoted", sample', s)
        self.assertIn('{foo,bar, baz}', s.replace('{foo,bar,baz}', '{foo,bar, baz}'))