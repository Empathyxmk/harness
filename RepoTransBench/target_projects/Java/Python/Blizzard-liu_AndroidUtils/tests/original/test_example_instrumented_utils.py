import unittest

class TestExampleInstrumentedUtils(unittest.TestCase):
    def test_use_app_context(self):
        # Stand-in for Android Context package name.
        app_context_package_name = "com.example.utils.test"
        self.assertEqual(app_context_package_name, "com.example.utils.test")