import unittest

class TestExampleInstrumentedUtilsPublic(unittest.TestCase):
    def test_use_app_context_public(self):
        app_context_package_name = "com.example.utils.test"
        self.assertNotEqual(app_context_package_name, "com.example.somethingelse")