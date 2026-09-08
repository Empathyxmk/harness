import unittest

class TestExampleInstrumentedAppPublic(unittest.TestCase):
    def test_use_app_context_public(self):
        # Should not equal unrelated package name
        app_context_package_name = "com.example.administrator.androidutils"
        self.assertNotEqual(app_context_package_name, "com.example.anotherpackage")