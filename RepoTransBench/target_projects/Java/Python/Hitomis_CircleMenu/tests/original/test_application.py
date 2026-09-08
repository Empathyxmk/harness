import unittest

class FakeApplication:
    pass

class TestApplication(unittest.TestCase):
    """
    Mimics the ApplicationTest in original Java code.
    """

    def setUp(self):
        self.application = FakeApplication()

    def test_can_create_application(self):
        self.assertIsNotNone(self.application)