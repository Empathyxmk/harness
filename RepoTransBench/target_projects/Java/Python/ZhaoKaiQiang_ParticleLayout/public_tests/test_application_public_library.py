import unittest

class TestApplicationPublicLibrary(unittest.TestCase):
    def test_application_public(self):
        class DummyApplication:
            pass
        class ApplicationTestCase:
            def __init__(self, app_cls):
                self.app_cls = app_cls
        test = ApplicationTestCase(DummyApplication)
        self.assertEqual(test.app_cls, DummyApplication)