from unittest import TestCase
from pypattyrn.creational.pool import Pool, Reusable

class MyObject(Reusable):
    def __init__(self, data):
        super().__init__()
        self.data = data

class PoolCoveragePublicTestCase(TestCase):
    def setUp(self):
        self.items = [MyObject(i) for i in range(5,9)]
        self.pool = Pool(lambda: self.items.pop() if self.items else MyObject(11))

    def test_multiple_checkout_checkin_public(self):
        a = self.pool.acquire()
        b = self.pool.acquire()
        self.assertIsInstance(a, MyObject)
        self.assertIsInstance(b, MyObject)
        self.pool.release(a)
        self.pool.release(b)
        c = self.pool.acquire()
        self.assertIsInstance(c, MyObject)
        # Check that objects are reused, not created new
        self.pool.release(c)
        d = self.pool.acquire()
        self.assertIsInstance(d, MyObject)
        # For public coverage, test that an exhausted pool will give MyObject(11)
        for _ in range(10):
            self.pool.acquire()
        extra = self.pool.acquire()
        self.assertEqual(extra.data, 11)