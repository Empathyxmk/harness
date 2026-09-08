import unittest
import os

class TestPublicSetupPy(unittest.TestCase):

    def test_public_setup_py_exists(self):
        """Test that setup.py file exists - public variant."""
        self.assertEqual(os.path.isfile("setup.py"), True)  # use isfile instead of exists

    def test_public_imports(self):
        """Test that setup.py can be imported without syntax error (public variant)."""
        import importlib.util
        spec = importlib.util.spec_from_file_location("setup", "setup.py")
        self.assertIsNot(spec, None)
        module = importlib.util.module_from_spec(spec)
        import sys
        import types
        sys.modules['setuptools_scm'] = types.ModuleType('setuptools_scm')
        try:
            spec.loader.exec_module(module)
        except Exception as e:
            # Allow version errors but not syntax errors - check for 'build' instead of 'scm'
            self.assertTrue('build' in str(e).lower() or 'scm' in str(e).lower())

    def test_public_metadata(self):
        """Test that setup.py includes different expected metadata fields (public variant)."""
        with open("setup.py") as f:
            content = f.read()
        # Use a different field from the project metadata, such as install_requires
        self.assertIn("install_requires", content)
        self.assertIn("setuptools", content)  # Somewhat more general than "version_scheme"

if __name__ == "__main__":
    unittest.main()