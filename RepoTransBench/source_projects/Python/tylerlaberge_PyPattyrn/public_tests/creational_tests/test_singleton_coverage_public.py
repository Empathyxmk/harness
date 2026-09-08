from unittest import TestCase
from pypattyrn.creational.singleton import Singleton

class PublicA(metaclass=Singleton):
    def __init__(self):
        self.name = "Alpha"

class PublicB(metaclass=Singleton):
    def __init__(self):
        self.name = "Beta"

class SingletonCoveragePublicTestCase(TestCase):
    def test_same_instance_public(self):
        a_1 = PublicA()
        a_2 = PublicA()
        b_1 = PublicB()
        b_2 = PublicB()
        self.assertEqual(id(a_1), id(a_2))
        self.assertEqual(id(b_1), id(b_2))

    def test_different_instance_public(self):
        a = PublicA()
        b = PublicB()
        self.assertNotEqual(id(a), id(b))
        self.assertEqual(a.name, "Alpha")
        self.assertEqual(b.name, "Beta")