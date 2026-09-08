import unittest

class FakeApplication:
    pass

class TestApplicationPublic(unittest.TestCase):
    def test_application_gets_instance(self):
        application = FakeApplication()
        self.assertIsNotNone(application)