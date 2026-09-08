import unittest
from pyzbar.scripts import read_zbar

class TestScriptsReadZbarPublic(unittest.TestCase):
    def test_create_argparser_and_help(self):
        parser = read_zbar.create_argparser()
        # Should contain -q/--quiet in description (different from existing verbose check)
        opts = [action.dest for action in parser._actions]
        self.assertIn("quiet", opts)
        self.assertIn("file", opts)

    def test_help_option(self):
        parser = read_zbar.create_argparser()
        # Changing how we check help: use get_help to ensure string contains 'usage'
        helptext = parser.format_help()
        self.assertIn("usage", helptext.lower())

if __name__ == "__main__":
    unittest.main()