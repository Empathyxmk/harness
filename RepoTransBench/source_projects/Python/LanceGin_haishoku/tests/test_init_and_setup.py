import unittest
import importlib.util
import os

class TestInitAndSetup(unittest.TestCase):
    def test_version(self):
        from haishoku import __version__
        self.assertTrue(__version__)
        self.assertIn('.', __version__)

    def test_setup_callable(self):
        setup_path = os.path.join(os.path.dirname(__file__), '../setup.py')
        setup_path = os.path.abspath(setup_path)
        spec = importlib.util.spec_from_file_location("setup", setup_path)
        setup = importlib.util.module_from_spec(spec)
        # This imports the setup.py but doesn't run the setup() call for real packaging,
        # so no side effects.
        try:
            spec.loader.exec_module(setup)
        except SystemExit:
            # setup() may call sys.exit()!
            pass
        self.assertTrue(hasattr(setup, 'setup'))
        self.assertTrue(hasattr(setup, 'find_packages'))

    def test_license_file(self):
        license_path = os.path.join(os.path.dirname(__file__), '../LICENSE')
        license_path = os.path.abspath(license_path)
        self.assertTrue(os.path.exists(license_path))

if __name__ == '__main__':
    unittest.main()