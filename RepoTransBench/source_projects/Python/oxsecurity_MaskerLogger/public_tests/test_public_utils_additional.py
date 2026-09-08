import unittest
from maskerlogger import utils

class TestUtilsAdditionalPublic(unittest.TestCase):
    def test_get_config_file_path_other_custom(self):
        # Use another custom config file name
        cfg = utils.get_config_file_path("anotherpublic.toml")
        self.assertTrue(cfg.endswith("anotherpublic.toml"))

    def test_get_config_file_path_folder_check(self):
        # Assert 'config' is actually part of the directory structure
        cfg = utils.get_config_file_path()
        self.assertTrue(any(part == "config" for part in cfg.split('/')) or any(part == "config" for part in cfg.split("\\")))

if __name__ == "__main__":
    unittest.main()