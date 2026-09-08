import unittest
from maskerlogger import utils

class TestUtilsPublic(unittest.TestCase):
    def test_get_config_file_path_non_default(self):
        # Different file name than in original test
        path = utils.get_config_file_path("alternative_config.toml")
        self.assertTrue(path.endswith("alternative_config.toml"))

    def test_get_config_file_path_contains_maskerlogger(self):
        # Verifies path has maskerlogger in it for coverage, different assertion focus
        path = utils.get_config_file_path()
        self.assertIn("maskerlogger", path)

if __name__ == "__main__":
    unittest.main()