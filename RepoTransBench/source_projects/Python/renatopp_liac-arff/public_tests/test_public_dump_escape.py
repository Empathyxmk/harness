import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import arff

class TestPublicDumpEscape(unittest.TestCase):
    def test_escape(self):
        obj = {
            "description": "Public dump escape",
            "relation": "escape_test",
            "attributes": [
                ("comment", "STRING"),
                ("list", ("ay", "bee!"))
            ],
            "data": [
                ["Hello, world!", "ay"],
                ["Special, chars!", "bee!"]
            ]
        }
        dump = arff.dumps(obj)
        self.assertIn('"Hello, world!"', dump)
        self.assertIn('bee!', dump)