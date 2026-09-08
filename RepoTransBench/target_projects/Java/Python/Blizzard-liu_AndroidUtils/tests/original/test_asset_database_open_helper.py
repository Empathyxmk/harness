import unittest
from unittest import mock

class AssetDatabaseOpenHelper:
    def __init__(self, ctx, name):
        self.ctx = ctx
        self.db_name = name

    def getDatabaseName(self):
        return self.db_name

    def getWritableDatabase(self):
        assets = self.ctx.getAssets()
        try:
            assets.open(self.db_name)
            return "database"  # fake return value
        except OSError:
            raise RuntimeError("Database cannot be opened")

class TestAssetDatabaseOpenHelper(unittest.TestCase):

    def test_get_database_name(self):
        ctx = mock.Mock()
        helper = AssetDatabaseOpenHelper(ctx, "mydb.db")
        self.assertEqual("mydb.db", helper.getDatabaseName())

    def test_get_writable_database_io_exception(self):
        ctx = mock.Mock()
        assets = mock.Mock()
        ctx.getAssets.return_value = assets
        assets.open.side_effect = OSError("fail")
        helper = AssetDatabaseOpenHelper(ctx, "fail.db")
        with self.assertRaises(RuntimeError):
            helper.getWritableDatabase()