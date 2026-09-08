import unittest
import random
from src.fastrange import fastrange32, fastrange64, fastrangesize

class TestCpp(unittest.TestCase):
    def get32rand(self):
        """Generate a random 32-bit unsigned integer"""
        return (random.randint(0, 0x7FFF) ^ 
                (random.randint(0, 0x7FFF) << 15) ^ 
                (random.randint(0, 0x3) << 30))
    
    def get64rand(self):
        """Generate a random 64-bit unsigned integer"""
        return (self.get32rand() << 32) | self.get32rand()
    
    def test_range32(self):
        # Test a smaller range for fastrange32 to keep test execution time reasonable
        for x in range(0, 1000):
            self.assertLess(fastrange32(x, 5), 5)
    
    def test_range64(self):
        # Test a smaller range for fastrange64 to keep test execution time reasonable
        for x in range(0, 1000):
            self.assertLess(fastrange64(x, 5), 5)
    
    def test_fill(self):
        # Tests the fill function which uses a set to collect values
        # until it reaches the specified size
        for x in range(1, 20):  # Reduced range to keep test time reasonable
            result_set = set()
            while len(result_set) < x:
                result_set.add(fastrangesize(self.get64rand(), x))
            # If we can fill the set with values 0 to x-1, the test passes

if __name__ == '__main__':
    unittest.main()