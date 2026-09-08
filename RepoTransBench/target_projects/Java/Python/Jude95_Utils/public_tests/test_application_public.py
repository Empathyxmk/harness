import unittest

class Application:
    # Mock of Android Application class for test stub
    pass

class ApplicationPublicTest(unittest.TestCase):
    def test_initialization(self):
        app = Application()
        self.assertIsInstance(app, Application)

if __name__ == "__main__":
    unittest.main()