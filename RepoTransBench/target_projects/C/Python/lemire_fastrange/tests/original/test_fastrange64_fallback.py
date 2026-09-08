import unittest
from src.fastrange import fastrange64, UINT64_MAX

class TestFastRange64Fallback(unittest.TestCase):
    def test_fallback(self):
        # These calls may trigger fallback code if present in fastrange.h
        max_val = UINT64_MAX
        m = 12345
        
        self.assertLess(fastrange64(max_val, m), m)
        self.assertEqual(fastrange64(0, m), 0)
        
        if m > 1:
            self.assertLess(fastrange64(max_val, m - 1), m - 1)

if __name__ == '__main__':
    unittest.main()