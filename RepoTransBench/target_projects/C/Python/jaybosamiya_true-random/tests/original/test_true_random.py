import unittest
from src.true_random import get_bit, get_byte, true_random

class TestTrueRandom(unittest.TestCase):
    def test_get_bit(self):
        """Test that get_bit returns either 0 or 1."""
        for _ in range(16):
            bit = get_bit()
            self.assertIn(bit, [0, 1], "get_bit should return either 0 or 1")
    
    def test_get_byte(self):
        """Test that get_byte function runs without errors."""
        for _ in range(4):
            b = get_byte()
            # Just checking the function doesn't crash, but let's also
            # verify the return is within the expected range
            self.assertTrue(0 <= b <= 255, "get_byte should return a value between 0 and 255")

if __name__ == "__main__":
    unittest.main()
    print("All tests passed.")