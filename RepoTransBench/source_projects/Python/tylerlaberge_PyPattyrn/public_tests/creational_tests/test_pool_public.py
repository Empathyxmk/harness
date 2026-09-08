from unittest import TestCase
from pypattyrn.creational.pool import Pool, Reusable

class TestResource(Reusable):
    def __init__(self, name):
        super().__init__()
        self.name = name

class PoolPublicTestCase(TestCase):
    def setUp(self):
        self.resources = [TestResource('R1'), TestResource('R2'), TestResource('R3')]
        self.pool = Pool(self.resources.pop)

    def test_acquire_release_public(self):
        x = self.pool.acquire()
        y = self.pool.acquire()
        self.assertIsInstance(x, TestResource)
        self.assertIsInstance(y, TestResource)
        self.pool.release(x)
        z = self.pool.acquire()
        self.assertIsInstance(z, TestResource)
        self.assertEqual(z.name, x.name)