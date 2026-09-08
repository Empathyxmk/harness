from unittest import TestCase
from pypattyrn.creational.prototype import Prototype

class Widget(Prototype):
    def __init__(self, value):
        super().__init__()
        self.value = value

class PrototypePublicTestCase(TestCase):
    def test_clone_public(self):
        w = Widget(123)
        w_clone = w.clone()
        self.assertIsInstance(w_clone, Widget)
        self.assertEqual(w_clone.value, 123)
        self.assertNotEqual(id(w), id(w_clone))

    def test_independent_public(self):
        w = Widget([9,8])
        w_clone = w.clone()
        w_clone.value.append(7)
        self.assertNotEqual(w.value, w_clone.value)