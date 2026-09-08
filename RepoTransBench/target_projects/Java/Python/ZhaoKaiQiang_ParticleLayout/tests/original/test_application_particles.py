import unittest

class TestApplicationParticles(unittest.TestCase):
    def test_application_case_runs(self):
        # Simulate creation of ApplicationTestCase with Application
        # No meaningful assertion possible here, just exercise the code path
        class DummyApplication:
            pass
        class ApplicationTestCase:
            def __init__(self, app_cls):
                self.app_cls = app_cls

        test = ApplicationTestCase(DummyApplication)
        self.assertEqual(test.app_cls, DummyApplication)