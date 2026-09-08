import unittest

class ExampleInstrumentedPublicTest(unittest.TestCase):
    def test_use_libyuv_context_public(self):
        appContextPackageName = "com.libyuv.util"
        self.assertIsNotNone(appContextPackageName)
        self.assertNotEqual("", appContextPackageName)