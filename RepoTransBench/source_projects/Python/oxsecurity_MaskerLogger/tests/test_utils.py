import unittest
from maskerlogger import utils

class TestUtils(unittest.TestCase):
    def test_get_config_file_path(self):
        path = utils.get_config_file_path()
        self.assertTrue(path.endswith("gitleaks.toml"))
        self.assertIn("config", path)

    def test_get_config_file_path_custom(self):
        cfg = utils.get_config_file_path("customfile.toml")
        self.assertTrue(cfg.endswith("customfile.toml"))

if __name__ == "__main__":
    unittest.main()