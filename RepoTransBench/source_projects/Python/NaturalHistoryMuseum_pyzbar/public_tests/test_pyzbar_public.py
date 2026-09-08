import unittest
from pyzbar.pyzbar import ZBarSymbol

class TestZBarSymbolPublic(unittest.TestCase):
    def test_enum_values(self):
        # Test that ZBarSymbol contains a non-QRCode symbol (e.g., CODE39)
        assert hasattr(ZBarSymbol, "CODE39")
        self.assertIsInstance(ZBarSymbol.CODE39, int)

    def test_all_symbols_includes_symbol(self):
        # Choose a symbol different from existing test, e.g., CODE93
        self.assertIn(ZBarSymbol.CODE93, ZBarSymbol.ALL)

if __name__ == "__main__":
    unittest.main()