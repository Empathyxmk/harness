import unittest

class PublicTestInitImports(unittest.TestCase):
    def test_imports(self):
        import greedypacker
        from greedypacker import BinManager, Item
        self.assertIsNotNone(greedypacker.BinManager)
        self.assertIsNotNone(greedypacker.Item)