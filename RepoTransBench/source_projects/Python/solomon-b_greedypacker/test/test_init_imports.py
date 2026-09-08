import unittest

class TestInitImports(unittest.TestCase):
    def test_imports(self):
        # Test that root module imports important objects
        import greedypacker
        from greedypacker import BinManager, Item
        self.assertTrue(hasattr(greedypacker, 'BinManager'))
        self.assertTrue(hasattr(greedypacker, 'Item'))