import unittest

class TestAssetDatabaseOpenHelperPublic(unittest.TestCase):
    def test_open_database_public(self):
        db_name = "another_public_test.db"
        self.assertTrue(db_name.startswith("another_"))