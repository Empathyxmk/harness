import unittest

class ExampleInstrumentedPublicTest(unittest.TestCase):
    def test_use_app_context_public(self):
        appContextPackageName = "com.hzl.libyuvdemo"
        self.assertNotEqual("com.nonexistent.package", appContextPackageName)
        self.assertIn("hzl", appContextPackageName)