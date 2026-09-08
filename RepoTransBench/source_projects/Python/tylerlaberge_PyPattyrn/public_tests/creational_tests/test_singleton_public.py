from unittest import TestCase
from pypattyrn.creational.singleton import Singleton


class SingletonPublicTestCase(TestCase):
    """
    Public unit testing class for the singleton design pattern (public data).
    """

    def setUp(self):
        """
        Initialize alternate testing data.
        """
        class AlphaSingleton(object, metaclass=Singleton):

            def __init__(self):
                self.value = 10

        class BetaSingleton(object, metaclass=Singleton):

            def __init__(self):
                self.value = 20

        self.AlphaSingleton = AlphaSingleton
        self.BetaSingleton = BetaSingleton

    def test_single_public(self):
        """
        Test instances from a single singleton class with alternate classes.
        """
        alpha1 = self.AlphaSingleton()
        alpha2 = self.AlphaSingleton()
        self.assertEqual(id(alpha1), id(alpha2))
        self.assertEqual(alpha1.value, 10)
        self.assertEqual(alpha2.value, 10)

    def test_multiple_public(self):
        """
        Test instances from multiple singleton classes with alternate classes.
        """
        alpha1 = self.AlphaSingleton()
        alpha2 = self.AlphaSingleton()
        beta1 = self.BetaSingleton()
        beta2 = self.BetaSingleton()
        self.assertEqual(id(alpha1), id(alpha2))
        self.assertEqual(id(beta1), id(beta2))
        self.assertNotEqual(id(alpha1), id(beta1))
        self.assertNotEqual(id(alpha2), id(beta2))

        # Additional check with public test data
        self.assertEqual(beta1.value, 20)
        self.assertEqual(beta2.value, 20)