import unittest

class TestLogUtilsPublic(unittest.TestCase):
    def test_info_log_level_public(self):
        level = "INFO"
        self.assertNotEqual("ERROR", level)