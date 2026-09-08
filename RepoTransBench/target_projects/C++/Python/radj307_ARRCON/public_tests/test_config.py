import unittest

class Config:
    def __init__(self):
        self._dict = {}

    def set(self, key, value):
        self._dict[key] = value

    def get(self, key):
        return self._dict.get(key, "")

class TestPublicConfig(unittest.TestCase):
    def test_public_set_and_get_value(self):
        cfg = Config()
        cfg.set("testKey123", "myTestValue456")
        self.assertEqual(cfg.get("testKey123"), "myTestValue456")

    def test_public_get_non_existing_returns_empty(self):
        cfg = Config()
        self.assertEqual(cfg.get("noSuchKey789"), "")