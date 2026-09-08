from unittest import TestCase
from pypattyrn.creational.factory import Factory, AbstractFactory

class Hat:
    def __init__(self, color):
        self.color = color

class Shoes:
    def __init__(self, size):
        self.size = size

class ClothingFactory(AbstractFactory):
    def get_hat(self):
        return Hat("blue")

    def get_shoes(self):
        return Shoes(10)

class FactoryPublicTestCase(TestCase):
    def setUp(self):
        self.factory = Factory(ClothingFactory())

    def test_factory_methods_public(self):
        hat = self.factory.get_hat()
        shoes = self.factory.get_shoes()
        self.assertIsInstance(hat, Hat)
        self.assertIsInstance(shoes, Shoes)
        self.assertEqual(hat.color, 'blue')
        self.assertEqual(shoes.size, 10)