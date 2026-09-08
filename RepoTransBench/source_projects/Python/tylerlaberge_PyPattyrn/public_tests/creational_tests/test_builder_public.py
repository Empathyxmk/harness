from unittest import TestCase

from abc import ABCMeta, abstractmethod
from pypattyrn.creational.builder import Director, Builder


class BuilderPublicTestCase(TestCase):
    """
    Public unit testing class for the Builder class (public test).
    """

    def setUp(self):
        """
        Initialize testing data.
        """

        class Car(object):
            def __init__(self):
                self.doors = None
                self.color = None

            def __repr__(self):
                return 'Doors: {0.doors} | Color: {0.color}'.format(self)

        class CarBuilder(Builder, metaclass=ABCMeta):
            def __init__(self):
                super().__init__(Car())
                self._register('doors', self._build_doors)
                self._register('color', self._build_color)

            @abstractmethod
            def _build_doors(self):
                pass

            @abstractmethod
            def _build_color(self):
                pass

        class SUVBuilder(CarBuilder):
            def _build_doors(self):
                self.constructed_object.doors = 'Four'

            def _build_color(self):
                self.constructed_object.color = 'Black'

        class CoupeBuilder(CarBuilder):
            def _build_doors(self):
                self.constructed_object.doors = 'Two'

            def _build_color(self):
                self.constructed_object.color = 'Red'

        self.suv_builder = SUVBuilder()
        self.coupe_builder = CoupeBuilder()

    def test_builder_public(self):
        """
        Test the build method with alternate data (public test).

        @raise AssertionError: If the test fails.
        """
        self.suv_builder.build('doors')
        self.suv_builder.build('color')
        self.assertEqual('Four', self.suv_builder.constructed_object.doors)
        self.assertEqual('Black', self.suv_builder.constructed_object.color)
        self.assertEqual('Doors: Four | Color: Black', str(self.suv_builder.constructed_object))

        self.coupe_builder.build('doors')
        self.coupe_builder.build('color')
        self.assertEqual('Two', self.coupe_builder.constructed_object.doors)
        self.assertEqual('Red', self.coupe_builder.constructed_object.color)
        self.assertEqual('Doors: Two | Color: Red', str(self.coupe_builder.constructed_object))


class DirectorPublicTestCase(TestCase):
    """
    Public unit testing class for the Director class (public test).
    """

    def setUp(self):
        """
        Initialize testing data.
        """

        class Car(object):
            def __init__(self):
                self.doors = None
                self.color = None

            def __repr__(self):
                return 'Doors: {0.doors} | Color: {0.color}'.format(self)

        class CarBuilder(Builder, metaclass=ABCMeta):
            def __init__(self):
                super().__init__(Car())
                self._register('doors', self._build_doors)
                self._register('color', self._build_color)

            @abstractmethod
            def _build_doors(self):
                pass

            @abstractmethod
            def _build_color(self):
                pass

        class SUVBuilder(CarBuilder):
            def _build_doors(self):
                self.constructed_object.doors = 'Four'

            def _build_color(self):
                self.constructed_object.color = 'Black'

        class CoupeBuilder(CarBuilder):
            def _build_doors(self):
                self.constructed_object.doors = 'Two'

            def _build_color(self):
                self.constructed_object.color = 'Red'

        class CarDirector(Director):
            def construct(self):
                self.builder.build('doors')
                self.builder.build('color')

        self.suv_builder = SUVBuilder()
        self.coupe_builder = CoupeBuilder()
        self.car_director = CarDirector()

    def test_construct_public(self):
        """
        Test the construct method with alternate data (public test).

        @raise AssertionError: If the test fails.
        """
        self.car_director.builder = self.suv_builder
        self.car_director.construct()
        suv = self.car_director.get_constructed_object()
        self.assertEqual('Four', suv.doors)
        self.assertEqual('Black', suv.color)
        self.assertEqual('Doors: Four | Color: Black', str(suv))

        self.car_director.builder = self.coupe_builder
        self.car_director.construct()
        coupe = self.car_director.get_constructed_object()
        self.assertEqual('Two', coupe.doors)
        self.assertEqual('Red', coupe.color)
        self.assertEqual('Doors: Two | Color: Red', str(coupe))