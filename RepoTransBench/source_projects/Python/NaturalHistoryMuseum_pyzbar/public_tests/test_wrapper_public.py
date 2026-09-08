import unittest

from pyzbar import wrapper

class TestWrapperPublic(unittest.TestCase):
    def test_get_symbol_name(self):
        # Using a different value for ZBarSymbol than the existing tests
        name = wrapper.get_symbol_name(13)  # e.g., 13 is PDF417
        self.assertIn("PDF417", name)

    def test_get_symbol_name_invalid(self):
        # Use an invalid code not typically tested
        name = wrapper.get_symbol_name(1000)
        self.assertEqual(name, "UNKNOWN")

if __name__ == "__main__":
    unittest.main()