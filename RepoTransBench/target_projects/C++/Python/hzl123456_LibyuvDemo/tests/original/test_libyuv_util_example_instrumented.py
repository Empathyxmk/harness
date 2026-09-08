import unittest

class ExampleInstrumentedTest(unittest.TestCase):
    def test_use_app_context(self):
        appContextPackageName = "com.libyuv.util"
        self.assertEqual("com.libyuv.util", appContextPackageName)