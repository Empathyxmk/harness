from unittest import TestCase
from abc import ABCMeta, abstractmethod
from pypattyrn.creational.builder import Builder

class CustomProduct(object):
    def __init__(self):
        self.part_a = None
        self.part_b = None

    def __repr__(self):
        return 'A: {0.part_a} | B: {0.part_b}'.format(self)

class GadgetBuilder(Builder, metaclass=ABCMeta):
    def __init__(self):
        super().__init__(CustomProduct())
        self._register('part_a', self._build_part_a)
        self._register('part_b', self._build_part_b)

    @abstractmethod
    def _build_part_a(self):
        pass

    @abstractmethod
    def _build_part_b(self):
        pass

class PhoneBuilder(GadgetBuilder):
    def _build_part_a(self):
        self.constructed_object.part_a = 'Screen'

    def _build_part_b(self):
        self.constructed_object.part_b = 'Battery'

class LaptopBuilder(GadgetBuilder):
    def _build_part_a(self):
        self.constructed_object.part_a = 'Keyboard'

    def _build_part_b(self):
        self.constructed_object.part_b = 'Trackpad'

class BuilderCoveragePublicTestCase(TestCase):
    def setUp(self):
        self.phone_builder = PhoneBuilder()
        self.laptop_builder = LaptopBuilder()

    def test_coverage_public_build(self):
        self.phone_builder.build('part_a')
        self.phone_builder.build('part_b')
        self.assertEqual('Screen', self.phone_builder.constructed_object.part_a)
        self.assertEqual('Battery', self.phone_builder.constructed_object.part_b)
        self.assertEqual('A: Screen | B: Battery', str(self.phone_builder.constructed_object))

        self.laptop_builder.build('part_a')
        self.laptop_builder.build('part_b')
        self.assertEqual('Keyboard', self.laptop_builder.constructed_object.part_a)
        self.assertEqual('Trackpad', self.laptop_builder.constructed_object.part_b)
        self.assertEqual('A: Keyboard | B: Trackpad', str(self.laptop_builder.constructed_object))