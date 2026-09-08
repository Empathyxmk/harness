import unittest
import os

class TestDemoScript(unittest.TestCase):
    def test_demo_file_exists(self):
        demo_py = os.path.join(os.path.dirname(__file__), '../demo/demo.py')
        self.assertTrue(os.path.exists(demo_py))

    def test_demo_png_exists(self):
        demo_png = os.path.join(os.path.dirname(__file__), '../demo/demo_01.png')
        self.assertTrue(os.path.exists(demo_png))

if __name__ == '__main__':
    unittest.main()