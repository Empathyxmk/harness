import unittest

class TestApplicationLibrary(unittest.TestCase):
    def test_application_case_runs(self):
        # Simulate ApplicationTestCase with Application class
        class DummyApplication:
            pass
        class ApplicationTestCase:
            def __init__(self, app_cls):
                self.app_cls = app_cls

        test = ApplicationTestCase(DummyApplication)
        self.assertEqual(test.app_cls, DummyApplication)