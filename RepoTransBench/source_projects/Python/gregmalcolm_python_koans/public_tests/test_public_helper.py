import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from runner import helper

class TestPublicHelper(unittest.TestCase):
    def test_public_cls_name_for_bool(self):
        self.assertEqual(helper.cls_name(True), "bool")

    def test_public_cls_name_for_tuple(self):
        self.assertEqual(helper.cls_name((1,)), "tuple")