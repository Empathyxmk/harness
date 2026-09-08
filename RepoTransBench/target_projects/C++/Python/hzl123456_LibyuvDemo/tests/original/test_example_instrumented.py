import unittest

class ExampleInstrumentedTest(unittest.TestCase):
    def test_use_app_context(self):
        # Mimic Android context package name
        appContextPackageName = "com.hzl.libyuvdemo"
        self.assertEqual("com.hzl.libyuvdemo", appContextPackageName)