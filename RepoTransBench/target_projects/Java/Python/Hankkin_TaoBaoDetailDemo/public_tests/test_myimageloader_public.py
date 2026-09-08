import unittest

class MyImageLoader:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MyImageLoader, cls).__new__(cls)
        return cls._instance
    @classmethod
    def getInstance(cls):
        return cls()

class TestMyImageLoaderPublic(unittest.TestCase):
    def test_public_singleton_instance_different_call_not_null(self):
        instanceA = MyImageLoader.getInstance()
        instanceB = MyImageLoader.getInstance()
        self.assertIsNotNone(instanceA)
        self.assertIsNotNone(instanceB)
        self.assertIs(instanceA, instanceB)